"""Use the Hermes gif_codex asciinema -> agg workflow on actual CLI events.
No desktop, terminal application or screen-capture API is accessed.
Code license pending author designation.
"""
from pathlib import Path
import argparse,json,subprocess,shlex,sys
ROOT=Path(__file__).resolve().parents[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('batch');ap.add_argument('--chapter',type=int);args=ap.parse_args()
 for n in ([args.chapter] if args.chapter else range(1,5)):
  folder=ROOT/'assets/recordings'/args.batch/f'A00{n}';rel=folder.relative_to(ROOT)
  command=shlex.join([sys.executable,'scripts/media/replay_course.py',str(rel)])
  cast=folder/'replay.cast';gif=folder/'demo.gif'
  if gif.exists():raise SystemExit('Refusing to replace existing GIF: '+str(folder))
  if not cast.exists():subprocess.run(['asciinema','rec','--headless','--return','-q','--window-size','100x34','--idle-time-limit','1','-c',command,str(cast)],check=True,cwd=ROOT)
  subprocess.run(['agg','-q','--select','0.1..100%','--font-family','Menlo,PingFang SC','--theme','dracula','--font-size','18','--speed','1','--idle-time-limit','1','--last-frame-duration','5',str(cast),str(gif)],check=True)
  result=subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,nb_frames','-of','json',str(gif)],capture_output=True,text=True,check=True)
  (folder/'gif-info.json').write_text(result.stdout)
  subprocess.run(['ffmpeg','-v','error','-i',str(gif),'-frames:v','1',str(folder/'demo-first.png')],check=True)
  # Last frame as static fallback; ffmpeg writes only the final decoded frame.
  subprocess.run(['ffmpeg','-v','error','-i',str(gif),'-update','1',str(folder/'demo-last.png')],check=True)
  print(f'A00{n}: {gif.stat().st_size} bytes; '+result.stdout.strip(),flush=True)
if __name__=='__main__':main()
