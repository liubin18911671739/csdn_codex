from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
def render(rows):
 s='# 专栏目录\n\n'
 for name,items in [('首季：Codex 应用实战', sorted([a for a in rows if a.get('season')==1],key=lambda a:a['order'])),('后续选题池',[a for a in rows if a.get('season')!=1])]:
  s+='## '+name+'\n\n'
  for a in items: s+=f"- {a['id']} | {a['title']} | {a['status']} | {a['validation']}\n"
  s+='\n'
 return s
if __name__=='__main__':
 (r/'planning/catalog.md').write_text(render(json.loads((r/'planning/articles.json').read_text())),encoding='utf8')
