"""Independent acceptance of generated course CLI artifacts (stdlib only).
Code license pending author designation.
"""
from pathlib import Path
import datetime,json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]
def main():
 batch=sys.argv[1];base=ROOT/'assets/recordings'/batch;checks=[]
 for ch in [2,3,4]:
  folder=base/f'A00{ch}';program=folder/'ledger.py';source=folder/'sample.csv';original=source.read_bytes()
  def run(*args):return subprocess.run([sys.executable,str(program),*map(str,args)],capture_output=True,text=True)
  p=run('--input',source);assert p.returncode==0 and all(x in p.stdout for x in ['5000.00','62.00','4938.00']),(ch,p.stderr)
  checks.append(f'A00{ch}: reference totals')
  with tempfile.TemporaryDirectory() as tmp:
   tmp=Path(tmp);data=tmp/'test.csv';header='日期,类型,类别,金额,备注\n'
   for field,bad in [('金额','-1'),('金额','NaN'),('金额','1.001'),('类型','退款'),('日期','not-a-date')]:
    row=dict(日期='2026-11-01',类型='收入',类别='工资',金额='1.00',备注='合成')
    row[field]=bad;data.write_text(header+','.join(row.values())+'\n',encoding='utf-8')
    p=run('--input',data);assert p.returncode!=0 and '2' in p.stderr,(ch,field,bad,p.stdout,p.stderr)
   data.write_text('金额\n1\n',encoding='utf-8');assert run('--input',data).returncode!=0
   data.write_text(header,encoding='utf-8-sig');p=run('--input',data);assert p.returncode==0 and '0.00' in p.stdout
   assert run('--input',tmp/'missing.csv').returncode!=0
   if ch>=3:
    output=tmp/'report.md';p=run('--input',source,'--output',output);assert p.returncode==0
    snapshot=output.read_bytes();assert '50.00' in snapshot.decode() and '12.00' in snapshot.decode()
    assert run('--input',source,'--output',output).returncode!=0 and output.read_bytes()==snapshot
    data.write_text(header+'2026-11-01,收入,工资,NaN,合成\n',encoding='utf-8')
    failed=tmp/'invalid-report.md';assert run('--input',data,'--output',failed).returncode!=0 and not failed.exists()
  assert source.read_bytes()==original
  checks.append(f'A00{ch}: invalid fields, empty BOM, missing input, input unchanged'+('; report export and no overwrite' if ch>=3 else ''))
 p=subprocess.run([sys.executable,'-m','unittest','-v'],cwd=base/'A004',text=True,capture_output=True)
 assert p.returncode==0,p.stderr
 checks.append('A004 generated unittest suite passed independently')
 result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,checks=checks,unittest_stdout=p.stdout,unittest_stderr=p.stderr)
 (base/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('\n'.join(checks));print(p.stderr)
if __name__=='__main__':main()
