"""Integrate verified CLI events into course drafts; never mark articles ready.
Code license pending author designation.
"""
import argparse,datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('batch');args=ap.parse_args()
 batch=args.batch;folder=ROOT/'assets/recordings'/batch
 articles=['001-start.md','002-setup.md','003-task.md','004-review.md']
 rows=json.loads((ROOT/'planning/articles.json').read_text())
 explanations=[
 '这个流程先确认解释器和目录，再做读写练习。环境记录文件来自真实运行；安装与登录没有重新操作，因此不在动图的验证范围内。',
 '第二章的终点是终端总额。先把读入、校验和金额累加做对，第三章再增加分类与导出，避免一次引入太多功能。',
 '导出前先验证完整输入；输出路径已存在时停止。图中的拒绝分支既要返回非零退出码，也要保证旧文件没有变化。',
 '测试通过只能说明这些用例通过。若某次运行没有失败，就如实展示通过结果，不为了教程戏剧性补造一次修复。']
 checks=[]
 for n,name in enumerate(articles,1):
  ident=f'A00{n}';part=folder/ident;meta=json.loads((part/'run.json').read_text())
  events=[json.loads(line) for line in (part/'run.jsonl').read_text().splitlines() if line.strip()]
  assert meta['exit_code']==0 and any(e.get('type')=='turn.completed' for e in events),ident
  assert (part/'demo.gif').exists() and (part/'demo-last.png').exists()
  # Skill timeline table + explicit diagnostics, including errors it does not render.
  timeline=['# '+ident+' CLI事件时间线','', '事件经过路径脱敏；命令或响应过长时表格节选，完整内容见同目录 run.jsonl。', '', '|序号|事件|内容节选|退出码|','|---|---|---|---|']
  count=0
  for event in events:
   item=event.get('item',{});typ=item.get('type','')
   if event.get('type')=='item.completed' and typ in {'command_execution','file_change','agent_message'}:
    count+=1
    body=item.get('command') if typ=='command_execution' else (item.get('text') if typ=='agent_message' else json.dumps(item.get('changes'),ensure_ascii=False))
    body=' '.join(str(body or '').split()).replace('|','\\|')
    timeline.append(f"|{count}|{typ}|{body[:200]}{'…' if len(body)>200 else ''}|{item.get('exit_code','—')}|")
   elif event.get('type') in {'error','turn.failed'}:
    timeline.append('|—|'+event['type']+'|'+json.dumps(event,ensure_ascii=False).replace('|','\\|')+'|—|')
  timeline.extend(['',f"进程退出码：{meta['exit_code']}。系统：{meta['system']}。",'', '## 标准错误原文','', '```text',(part/'stderr.txt').read_text().rstrip() or '本次标准错误为空。','```'])
  (part/'timeline.md').write_text('\n'.join(timeline)+'\n')
  hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in part.iterdir() if p.is_file() and p.name!='sha256.json'}
  (part/'sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
  path=ROOT/'articles'/name;s=path.read_text()
  s=s.replace('图中的返回分支要求先保留错误。不要为了看到成功提示而删去失败数据或放宽断言。',explanations[n-1])
  if n>1:
   start=s.index('## 三、准备环境与练习材料');end=s.index('## 四、把任务交给 Codex')
   previous=f'ch0{n-1}' if n>2 else '空目录'
   prep=f'''## 三、准备本章输入\n\n先完成第一章环境检查。本章只用 Python 标准库，不重复安装 CLI 或扩展。新建独立目录，放入合成 sample.csv；'''
   prep+=('从零让 Codex 新建 ledger.py。' if n==2 else f'复制上一章 {previous} 的 ledger.py，本章仅修改副本。')
   prep+=f'本次真实运行的交付文件在 [本章素材目录](../assets/recordings/{batch}/{ident}/README.md)，也可先跟着提示词完成，再与记录对照。\n\n'
   s=s[:start]+prep+s[end:]
  else:
   s=re.sub(r'练习附件位于仓库.*?类型只接受收入和支出。','本章从空目录开始，只创建 UTF-8 的 input.txt，内容为“环境练习”。不需要提前复制收支工具。',s,flags=re.S)
   s=s.replace('先自己算一组小数据，再观察程序。原件不变、金额一致、错误能定位、输出可重开才算交付。第四章使用 python3 -m unittest -v 执行配套测试；失败时记录命令、异常和实际值。','重新打开 environment.md，核对输入原文和实际版本，确认 input.txt 未变、没有无关文件。把练习换到另一个空目录再试；不要删除旧文件来制造一次“首次运行”。')
  start=s.index('## 四、把任务交给 Codex');code_start=s.index('```text',start);code_end=s.index('```',code_start+7)
  s=s[:code_start]+'```text\n'+(part/'prompt.txt').read_text()+'\n'+s[code_end:]
  s=s.replace('本文保持草稿，无虚构截图或Codex会话。','本文有独立 Codex CLI 运行证据；事件重放不是桌面截图，Windows仍待实测，保持草稿。')
  section=f'''## 八、实际 CLI 运行：看动图，也看证据\n\n![{ident} Codex CLI真实事件重放](../assets/recordings/{batch}/{ident}/demo.gif)\n\n这张动图使用 Hermes 的 gif_codex 技能工作流制作：先真实执行 codex exec --json，再通过 asciinema 与 agg 渲染事件重放。它经过路径脱敏、长输出节选和重新计时，**不是 Codex 桌面、IDE 或安装界面的截图**。\n\n静态阅读可看[末帧](../assets/recordings/{batch}/{ident}/demo-last.png)；逐条核对可看[时间线](../assets/recordings/{batch}/{ident}/timeline.md)、[原始事件脱敏版](../assets/recordings/{batch}/{ident}/run.jsonl)和[标准错误](../assets/recordings/{batch}/{ident}/stderr.txt)。原始未脱敏记录另存在不入库的工作目录。\n\n{explanations[n-1]}\n\n'''
  s=s.replace('## 来源与权利',section+'## 来源与权利')
  if n==1:s=s.replace('Codex 另输出 PATH 别名创建权限警告','Codex 另输出 PATH 别名创建权限警告')
  path.write_text(s)
  items=sorted(p.name for p in part.iterdir() if p.is_file())
  (part/'README.md').write_text('# '+ident+' 独立CLI运行素材\n\n批次：'+batch+'。仅本机运行，不代表Windows验证。\n\n'+ '\n'.join('- `'+name+'`' for name in items)+'\n\nGIF为事件重放，long output有节选，完整错误保留。生成代码授权待作者指定，不声明开放许可。\n')
  a=rows[n-1];a['status']='draft';a['revision']='ledger-cli-gif-v1';a['validation']='macOS独立Codex CLI已运行并生成事件重放；Windows及安装界面待验证'
  a['recording']={'batch':batch,'kind':'cli_event_replay','directory':str(part.relative_to(ROOT))}
  for ext in ['demo.gif','demo-last.png','timeline.md','run.jsonl','run.json','README.md']:
   p=str((part/ext).relative_to(ROOT))
   if p not in a['resources']:a['resources'].append(p)
  note=f'''\n## 独立 CLI 实跑与 GIF\n\n批次 {batch}；技能 gif_codex（Hermes，MIT）。执行根在独立临时目录。宿主系统 {meta['system']}；录制使用 asciinema 3.2.1、agg 1.9.0，字体 Menlo 与 PingFang SC。命令退出码 {meta['exit_code']}，事件包含 turn.completed。\n\nGIF 为脱敏事件重放，时间重新编排，长输出有节选；标准错误未清除。CLI任务和逐项命令见 assets/recordings/{batch}/{ident}/timeline.md。原始未脱敏记录在忽略目录 examples/work/gif-codex/{batch}。\n\n文风审查：减少重复安装说明、明确本章输入和成果，分开真实运行与教学参考。仍待：Windows、安装与登录界面、IDE实测、正文和代码权利登记。保持draft。\n'''
  with (ROOT/a['validation_file']).open('a') as f:f.write(note)
  checks.append({'article':ident,'exit_code':meta['exit_code'],'completed_events':count})
 (ROOT/'planning/articles.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 (folder/'manifest.json').write_text(json.dumps({'batch':batch,'skill':'Hermes gif_codex','kind':'cli_event_replay','chapters':checks},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(checks,ensure_ascii=False))
if __name__=='__main__':main()
