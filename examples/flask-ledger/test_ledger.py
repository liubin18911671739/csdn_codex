from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent
CLI = ROOT / "ledger.py"
HEADER = "日期,类型,类别,金额,备注\n"
SAMPLE_REPORT = (
    "收入：5000.00\n支出：62.00\n结余：4938.00\n"
    "\n## 支出分类汇总\n\n餐饮：50.00\n交通：12.00\n"
)
EMPTY_REPORT = "收入：0.00\n支出：0.00\n结余：0.00\n\n## 支出分类汇总\n\n"


class LedgerCLITest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.sample = (ROOT / "sample.csv").read_bytes()

    def tearDown(self):
        self.assertEqual((ROOT / "sample.csv").read_bytes(), self.sample)

    def run_cli(self, source, output=None):
        before = source.read_bytes() if source.exists() else None
        command = [sys.executable, str(CLI), "--input", str(source)]
        if output is not None:
            command.extend(["--output", str(output)])
        result = subprocess.run(command, cwd=self.work, capture_output=True,
                                text=True, encoding="utf-8", timeout=10)
        if before is not None:
            self.assertEqual(source.read_bytes(), before, "CLI 修改了原输入")
        else:
            self.assertFalse(source.exists())
        return result

    def write_input(self, text, encoding="utf-8"):
        source = self.work / "input.csv"
        source.write_text(text, encoding=encoding)
        return source

    def assert_success(self, result, expected):
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.stdout, expected)

    def test_sample_totals_and_categories(self):
        self.assert_success(self.run_cli(ROOT / "sample.csv"), SAMPLE_REPORT)

    def test_bom(self):
        source = self.work / "bom.csv"
        source.write_bytes(b"\xef\xbb\xbf" + self.sample)
        self.assert_success(self.run_cli(source), SAMPLE_REPORT)

    def test_empty_tables(self):
        for text in ("", HEADER):
            with self.subTest(text=text):
                self.assert_success(self.run_cli(self.write_input(text)), EMPTY_REPORT)

    def test_invalid_records(self):
        cases = [
            ("日期,类型,类别,备注\n", "缺列", "第1行"),
            (HEADER + "2026-11-01,收入,工资\n", "记录缺列", "第2行"),
            (HEADER + "2026-02-30,收入,工资,1.00,测试\n", "非法日期", "第2行"),
            (HEADER + "2026-11-01,转账,工资,1.00,测试\n", "非法类型", "第2行"),
            (HEADER + "2026-11-01,支出,餐饮,-1.00,测试\n", "金额不能为负数", "第2行"),
            (HEADER + "2026-11-01,支出,餐饮,NaN,测试\n", "金额必须为有限数值", "第2行"),
            (HEADER + "2026-11-01,支出,餐饮,1.001,测试\n", "金额超过两位小数", "第2行"),
        ]
        for text, message, line in cases:
            with self.subTest(message=message):
                output = self.work / "invalid-report.txt"
                result = self.run_cli(self.write_input(text), output)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertIn(message, result.stderr)
                self.assertIn(line, result.stderr)
                self.assertFalse(output.exists())

    def test_missing_input(self):
        output = self.work / "report.txt"
        result = self.run_cli(self.work / "missing.csv", output)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("读取失败", result.stderr)
        self.assertFalse(output.exists())

    def test_generate_report(self):
        output = self.work / "report.txt"
        result = self.run_cli(ROOT / "sample.csv", output)
        self.assert_success(result, "")
        self.assertEqual(output.read_bytes(), SAMPLE_REPORT.encode("utf-8"))

    def test_refuse_overwrite(self):
        output = self.work / "report.txt"
        original = b"existing report\x00\xff"
        output.write_bytes(original)
        result = self.run_cli(ROOT / "sample.csv", output)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("报告写入失败", result.stderr)
        self.assertEqual(output.read_bytes(), original)

    def test_refuse_output_equal_to_input(self):
        source = self.work / "input.csv"
        source.write_bytes(self.sample)
        result = self.run_cli(source, source)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("报告写入失败", result.stderr)
        self.assertEqual(source.read_bytes(), self.sample)


if __name__ == "__main__":
    unittest.main()
