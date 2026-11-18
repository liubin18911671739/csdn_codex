from pathlib import Path
import argparse, shutil, json
p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('target'); p.add_argument('--apply',action='store_true'); a=p.parse_args()
s,t=Path(a.source).resolve(),Path(a.target).resolve()
if not s.is_dir(): p.error('source must be a directory')
if t==s or s in t.parents: p.error('target must be outside source')
if t.exists(): p.error('target already exists')
files=sorted(x for x in s.iterdir() if x.is_file() and not x.is_symlink())
plan={x.name:'整理_'+x.name for x in files}
for old,new in plan.items(): print(old+' -> '+new)
if a.apply:
 t.mkdir(parents=True)
 for x in files: shutil.copy2(x,t/plan[x.name])
 (t/'manifest.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
