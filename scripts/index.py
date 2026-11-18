from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]; rows=json.loads((r/'planning/articles.json').read_text())
s='# 专栏完整目录\n\n'
for a in rows:
 s+=f"- {a['id']} | {a['unit']} | {a['title']} | {a['status']} | {a['validation']}\n"
(r/'planning/catalog.md').write_text(s,encoding='utf8')
