from pathlib import Path
import json,re
r=Path(__file__).resolve().parents[1]; rows=json.loads((r/'planning/articles.json').read_text())
assert len(rows)==60 and len({a['id'] for a in rows})==60
for a in rows:
 for k in ['id','title','status','target_os','cost','validation','sources','resources','book_chapter','outcome']: assert k in a,(a,k)
 for p in a.get('resources',[])+([a['file']] if 'file' in a else []): assert (r/p).is_file(),p
for f in r.rglob('*.md'):
 if '.git' in f.parts: continue
 for url in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if not re.match(r'^[a-z]+:',url) and not url.startswith('#'): assert (f.parent/url.split('#')[0]).exists(),(f,url)
assert sum(a['status']=='draft' for a in rows)==3
print('PASS: 60 unique articles, 3 drafts, metadata, resources and local links')
