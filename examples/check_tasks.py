# License: authorization pending; publication blocked until author approval.
"""Read-only strict checker for the A001 reference table, not a semantic evaluator."""
import sys
from pathlib import Path
EXPECTED=[['任务','负责人','截止时间'],['整理图片','小林','周五'],['报告','小周','待确认'],['资料备份','待确认','待确认']]
def check(path):
 rows=[]
 for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
  if not line.strip(): continue
  if not line.strip().startswith('|'): raise ValueError('Unexpected non-table text')
  cells=[c.strip() for c in line.strip().strip('|').split('|')]
  if cells and all(c and set(c)<=set('-: ') for c in cells): continue
  rows.append(cells)
 if rows!=EXPECTED: raise ValueError('Fields or row order differ from the reference')
if __name__=='__main__':
 try:
  if len(sys.argv)!=2: raise ValueError('Usage: python check_tasks.py tasks.md')
  check(sys.argv[1])
 except (OSError,UnicodeError,ValueError) as exc:
  print(str(exc),file=sys.stderr);sys.exit(1)
 print('PASS: strict reference match')
