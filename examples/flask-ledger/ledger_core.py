# Code license: pending author designation; publication not approved.
import csv
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import re

COLUMNS = ("日期", "类型", "类别", "金额", "备注")


class LedgerError(ValueError):
    pass


def analyze(stream):
    income = Decimal("0.00")
    expense = Decimal("0.00")
    categories = {}
    errors = []
    try:
        reader = csv.reader(stream, strict=True)
        header = next(reader, None)
        if header is not None:
            missing = [name for name in COLUMNS if name not in header]
            if missing:
                errors.append("CSV 第1行：缺列：" + "、".join(missing))
            else:
                positions = {name: header.index(name) for name in COLUMNS}
                while True:
                    line = reader.line_num + 1
                    row = next(reader, None)
                    if row is None:
                        break
                    if not row:
                        continue
                    if len(row) < len(header):
                        errors.append(f"CSV 第{line}行：记录缺列")
                        continue
                    fields = {name: row[index].strip() for name, index in positions.items()}
                    problems = []
                    if fields["类型"] not in ("收入", "支出"):
                        problems.append("非法类型")
                    try:
                        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fields["日期"]):
                            raise ValueError
                        date.fromisoformat(fields["日期"])
                    except ValueError:
                        problems.append("非法日期")
                    if not fields["类别"]:
                        problems.append("空类别")
                    try:
                        amount = Decimal(fields["金额"])
                        if not amount.is_finite():
                            problems.append("金额必须为有限数值（不允许 NaN 或无穷大）")
                        elif amount < 0:
                            problems.append("金额不能为负数")
                        elif amount.as_tuple().exponent < -2:
                            problems.append("金额超过两位小数")
                    except InvalidOperation:
                        problems.append("非法金额")
                    if problems:
                        errors.append(f"CSV 第{line}行：" + "；".join(problems))
                        continue
                    with localcontext() as context:
                        context.prec = max(28, amount.adjusted() + 4,
                                           income.adjusted() + 4, expense.adjusted() + 4)
                        if fields["类型"] == "收入":
                            income += amount
                        else:
                            expense += amount
                            category = fields["类别"]
                            categories[category] = categories.get(category, Decimal("0.00")) + amount
    except (OSError, UnicodeError, csv.Error) as exc:
        line = reader.line_num if "reader" in locals() else 1
        errors.append(f"CSV 第{line}行：读取失败：{exc}")
    if errors:
        raise LedgerError("\n".join(errors))
    with localcontext() as context:
        context.prec = max(28, income.adjusted() + 4, expense.adjusted() + 4)
        balance = income - expense
        lines = [f"收入：{income:.2f}", f"支出：{expense:.2f}",
                 f"结余：{balance:.2f}", "", "## 支出分类汇总", ""]
        lines.extend(f"{category}：{amount:.2f}" for category, amount in categories.items())
        report = "\n".join(lines) + "\n"
    return {"income": f"{income:.2f}", "expense": f"{expense:.2f}",
            "balance": f"{balance:.2f}", "categories": {k: f"{v:.2f}" for k, v in categories.items()},
            "report": report}
