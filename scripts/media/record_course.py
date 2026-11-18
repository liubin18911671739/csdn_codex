"""Record isolated Codex CLI course tasks. No desktop/window access.
Code license pending author designation. Uses gif_codex workflow (MIT skill).
"""
import argparse,datetime,json,os,platform,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
COMMON='只操作当前练习目录，不访问其他项目、账号配置或私人文件。只用Python标准库，不安装依赖，不使用浏览器、桌面控制或网络工具。先简述计划，再真正执行命令，中文回复简短。不能运行时如实说明，不伪造输出。已有目标不要覆盖。'
PROMPTS=[
'读取input.txt；实际运行codex --version和python3 --version，只新建environment.md，写入输入内容与实际版本。用Python重新读取验证文件与输入一致，报告结果。',
'读取sample.csv，从零新建ledger.py。用argparse接受--input；csv按utf-8-sig读取，列为日期、类型、类别、金额、备注。用Decimal按收入和支出累加，打印收入、支出、结余两位小数。不导出报告、不做分类汇总。记录缺列、非法类型、非法日期、空类别、负数、NaN或超过两位小数为带CSV行号的错误，退出码非零。空表输出零。真正运行python3 ledger.py --input sample.csv，核对5000.00、62.00、4938.00。不要创建其他说明文件。',
'读取已有ledger.py和sample.csv，在本章副本增量增加分类汇总以及可选--output report.md。不指定输出则打印，指定输出用排他创建，目标已存在返回非零且不改旧文件。全部输入验证后才写文件。先新建report.md并读回，再重复执行验证拒绝覆盖、报告字节和输入字节不变。分类餐饮50.00、交通12.00。保留命令输出，最后列出改动和实际检查。只修改ledger.py并新建report.md。',
'读取本章ledger.py和sample.csv，仅新建test_ledger.py，用标准库unittest和临时目录以子进程调用CLI。测试样例总额与分类、BOM、空表、缺列、非法日期或类型、负数与NaN及三位小数、输入不存在、报告生成、拒绝覆盖和原输入不变。手工预期不能随程序改动。运行python3 -m unittest -v。若失败，先保留失败输出再修ledger.py并重跑；没有失败不要构造修复故事。']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--batch');ap.add_argument('--chapter',type=int,choices=range(1,5),required=True);args=ap.parse_args()
 batch=args.batch or datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 public=ROOT/'assets/recordings'/batch;private=ROOT/'examples/work/gif-codex'/batch
 work=Path('/private/tmp/csdn-gif-codex')/batch/f'ch0{args.chapter}'
 work.mkdir(parents=True,exist_ok=False);private.mkdir(parents=True,exist_ok=True);out=public/f'A00{args.chapter}';out.mkdir(parents=True,exist_ok=False)
 if args.chapter==1:(work/'input.txt').write_text('环境练习\n',encoding='utf-8')
 else:
  shutil.copy2(ROOT/'examples/ledger/ch02/sample.csv',work/'sample.csv')
  if args.chapter>2:shutil.copy2(work.parent/f'ch0{args.chapter-1}/ledger.py',work/'ledger.py')
 prompt=COMMON+'\n\n'+PROMPTS[args.chapter-1];(out/'prompt.txt').write_text(prompt,encoding='utf-8')
 cmd=['codex','exec','--json','--ephemeral','--skip-git-repo-check','-s','workspace-write','-C',str(work),'-']
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 with (private/f'A00{args.chapter}.jsonl').open('w') as stdout,(private/f'A00{args.chapter}.stderr').open('w') as stderr:
  try:p=subprocess.run(cmd,input=prompt,text=True,stdout=stdout,stderr=stderr,timeout=300);code=p.returncode
  except subprocess.TimeoutExpired:code=124
 meta=dict(chapter=args.chapter,batch=batch,system=platform.platform(),python=platform.python_version(),started_utc=started,duration_seconds=round(time.monotonic()-t,2),exit_code=code,kind='Codex CLI event replay; not desktop screenshot',command=cmd,work=str(work))
 # Recursive path redaction; preserve failures. Original records stay in ignored examples/work.
 def clean(s):return s.replace(str(work.parent),'[WORK]').replace(str(ROOT),'[PROJECT]').replace(str(Path.home()),'~')
 (out/'run.jsonl').write_text(clean((private/f'A00{args.chapter}.jsonl').read_text()),encoding='utf-8')
 (out/'stderr.txt').write_text(clean((private/f'A00{args.chapter}.stderr').read_text()),encoding='utf-8')
 (out/'run.json').write_text(clean(json.dumps(meta,ensure_ascii=False,indent=2)),encoding='utf-8')
 print(json.dumps(dict(batch=batch,chapter=args.chapter,exit_code=code,duration=meta['duration_seconds']),ensure_ascii=False),flush=True)
 if code==0:
  for f in work.iterdir():
   if f.is_file() and f.suffix in {'.py','.csv','.md','.txt'}:shutil.copy2(f,out/f.name)
 raise SystemExit(code)
if __name__=='__main__':main()
