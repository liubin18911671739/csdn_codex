"""Readable, labelled event replay adapted from Hermes gif_codex (MIT).
Source: ~/.hermes/profiles/ollama/skills/autonomous-ai-agents/gif_codex.
Changes: preserve error/status events, no unconditional success, explicit excerpts,
ASCII markers, final task summary. Not a native application recording.
"""
import argparse,json,time,unicodedata
from pathlib import Path

def wrap(text,width=94):
 line='';size=0
 for c in text:
  n=2 if unicodedata.east_asian_width(c) in 'WF' else 1
  if size+n>width:yield line;line='';size=0
  line+=c;size+=n
 yield line

def emit(text,color='37',limit=None):
 lines=[part for line in str(text).splitlines() for part in wrap(line)]
 shown=lines if limit is None else lines[:limit]
 for line in shown:print(f'\033[{color}m{line}\033[0m',flush=True)
 if limit and len(lines)>limit:print(f'... excerpt: {len(lines)-limit} lines omitted; full run.jsonl retained',flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('folder');args=ap.parse_args();folder=Path(args.folder)
 meta=json.loads((folder/'run.json').read_text());events=[json.loads(x) for x in (folder/'run.jsonl').read_text().splitlines() if x.strip()]
 print('\033[2J\033[H',end='');emit(f"A00{meta['chapter']} | CODEX CLI EVENT REPLAY",'36;1')
 emit('Recorded CLI events, re-timed and excerpted. NOT a desktop screenshot.','33')
 emit('Local macOS run; published paths redacted.');time.sleep(.5)
 emit('TASK: '+(folder/'prompt.txt').read_text().split('\n\n',1)[-1],limit=7);time.sleep(1)
 command_count=0;completed=False
 for event in events:
  kind=event.get('type','')
  if kind in {'error','turn.failed'}:
   emit(json.dumps(event,ensure_ascii=False),'31');time.sleep(.5)
  if kind=='turn.completed':completed=True
  if kind!='item.completed':continue
  item=event.get('item',{});typ=item.get('type')
  if typ=='command_execution':
   command_count+=1;emit('\n$ '+str(item.get('command','')),'36',10)
   emit(item.get('aggregated_output',''),limit=16)
   emit('command exit code: '+str(item.get('exit_code')),'33');time.sleep(.8)
  elif typ=='file_change':
   emit('\nFILE CHANGES','33;1')
   for change in item.get('changes',[]):emit(str(change.get('kind'))+' '+str(change.get('path')),'33')
   time.sleep(.5)
  elif typ=='agent_message':emit('\nAGENT: '+item.get('text',''),'37',14);time.sleep(.6)
 stderr=(folder/'stderr.txt').read_text().strip()
 if stderr:emit('\nSTDERR (retained in full in stderr.txt):\n'+stderr,'31',8);time.sleep(.8)
 print('\033[2J\033[H',end='');emit(f"A00{meta['chapter']} | EVENT REPLAY SUMMARY",'36;1')
 emit('Not a desktop screenshot. No installation/login screen was recorded.','33')
 emit(f"CLI exit: {meta['exit_code']} | turn.completed: {completed} | commands: {command_count}",'32' if meta['exit_code']==0 and completed else '31')
 # Show actual final agent response, not a fabricated PASS banner.
 messages=[e.get('item',{}).get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 if messages:emit(messages[-1],limit=20)
 emit('Evidence: run.jsonl / stderr.txt / timeline.md','33');time.sleep(1)
if __name__=='__main__':main()
