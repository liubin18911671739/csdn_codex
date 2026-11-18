# Code license: pending author designation; not approved for publication.
import argparse,csv,sys
from pathlib import Path
from decimal import Decimal,InvalidOperation
from datetime import date

def summarize(path):
 totals={'收入':Decimal(0),'支出':Decimal(0)}; categories={}
 with Path(path).open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f)
  if not {'日期','类型','类别','金额','备注'}<=set(reader.fieldnames or []): raise ValueError('缺少必需列')
  for n,row in enumerate(reader,2):
   try:
    date.fromisoformat(row['日期'])
    kind=row['类型']; category=row['类别'].strip()
    amount=Decimal(row['金额'])
    if kind not in totals or not category or not amount.is_finite() or amount<0 or amount.as_tuple().exponent < -2: raise ValueError('字段无效')
   except (ValueError,InvalidOperation,AttributeError,TypeError) as exc: raise ValueError(f'第{n}行无效') from exc
   totals[kind]+=amount;key=(kind,category);categories[key]=categories.get(key,Decimal(0))+amount
 return totals,categories

def report(totals,categories):
 lines=['# 收支报告',f"收入：{totals['收入']:.2f}",f"支出：{totals['支出']:.2f}",f"结余：{totals['收入']-totals['支出']:.2f}"]
 for (kind,category),value in sorted(categories.items()): lines.append(f'{kind} / {category}：{value:.2f}')
 return '\n\n'.join(lines)+'\n'

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output');args=parser.parse_args()
 try:
  text=report(*summarize(args.input))
  if args.output:
   with Path(args.output).open('x',encoding='utf-8') as f:f.write(text)
  else:print(text,end='')
 except (OSError,ValueError) as exc:print(str(exc),file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
