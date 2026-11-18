from pathlib import Path
import json,re
from index import render
r=Path(__file__).resolve().parents[1]
def validate(rows):
 ids=[a['id'] for a in rows]
 assert len(ids)==len(set(ids)), 'duplicate ID'
 season=[a for a in rows if a.get('season')==1]
 assert sorted(a['order'] for a in season)==list(range(1,25)), 'season order'
 for a in rows:
  if a.get('file'):
   assert '```mermaid' in (r/a['file']).read_text(), 'missing diagram'
  assert a['status'] in {'planned','draft','ready','published'}
  for dep in a['prerequisites']:
   assert dep in ids and dep!=a['id']
   parent=next(x for x in rows if x['id']==dep)
   assert parent['season']==a['season'] and parent['order']<a['order']
  for p in a.get('resources',[])+a['materials']+([a['file']] if a.get('file') else [])+([a['validation_file']] if a.get('validation_file') else []):
   assert (r/p).is_file(), p
  if a['status'] in {'ready','published'}:
   evidence=json.loads((r/a['validation_file']).with_suffix('.json').read_text())
   assert evidence['article']==a['id'] and evidence['technical_pass'] is True and evidence['sources_pass'] is True
   assert evidence['environment'] and evidence['actual_outputs'] and evidence['source_checks']
rows=json.loads((r/'planning/articles.json').read_text())
validate(rows)
assert (r/'planning/catalog.md').read_text()==render(rows)
for f in r.rglob('*.md'):
 if '.git' in f.parts: continue
 for url in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if not re.match(r'^[a-z]+:',url) and not url.startswith('#'): assert (f.parent/url.split('#')[0]).exists(),(f,url)
for mutation in ['order','resource','evidence']:
 sample=json.loads(json.dumps(rows))
 if mutation=='order': sample[1]['order']=1
 elif mutation=='resource': sample[0]['materials']=['missing-fixture']
 else: sample[0]['status']='ready'
 try: validate(sample)
 except (AssertionError,FileNotFoundError,TypeError): pass
 else: raise AssertionError('invalid fixture accepted: '+mutation)
print('PASS: season order, metadata, resources, evidence guards, links and catalog')
