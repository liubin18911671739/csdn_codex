# Code license pending author designation.
import unittest,tempfile
from pathlib import Path
from decimal import Decimal
from ledger import summarize,report
class LedgerTests(unittest.TestCase):
 def test_sample(self):
  totals,categories=summarize(Path(__file__).with_name('sample.csv'))
  self.assertEqual(totals['支出'],Decimal('62.00'))
  self.assertIn('4938.00',report(totals,categories))
 def test_invalid_and_bom(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a.csv';header='日期,类型,类别,金额,备注\n'
   for amount in ['-1','NaN','1.001']:
    p.write_text(header+f'2026-11-01,收入,工资,{amount},测试\n')
    with self.assertRaises(ValueError):summarize(p)
   p.write_text(header,encoding='utf-8-sig');self.assertEqual(summarize(p)[0]['收入'],0)
   p.write_text('金额\n1\n')
   with self.assertRaises(ValueError):summarize(p)
   with self.assertRaises(FileNotFoundError):summarize(Path(d)/'missing')
if __name__=='__main__':unittest.main()
