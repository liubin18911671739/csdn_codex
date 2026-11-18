# Code license: pending author designation; publication not approved.
import argparse
import sys
from ledger_core import COLUMNS, LedgerError, analyze


def main():
    parser = argparse.ArgumentParser(description="计算收入、支出和结余")
    parser.add_argument("--input", required=True, help="CSV 文件路径")
    parser.add_argument("--output", help="报告路径（仅创建新文件）")
    args = parser.parse_args()
    try:
        with open(args.input, encoding="utf-8-sig", newline="") as stream:
            report = analyze(stream)["report"]
    except LedgerError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"CSV 第1行：读取失败：{exc}", file=sys.stderr)
        return 1
    if args.output:
        try:
            with open(args.output, "x", encoding="utf-8", newline="\n") as stream:
                stream.write(report)
        except (OSError, UnicodeError) as exc:
            print(f"报告写入失败：{exc}", file=sys.stderr)
            return 1
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
