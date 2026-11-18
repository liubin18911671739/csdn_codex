# 原生截图采集

由作者手动操作，图片放入 incoming，保留原图，不覆盖。截图注明macOS或Windows、客户端版本和日期。隐藏账号、密钥、私人路径及其他会话。

1. A001：在独立目录检查 codex --version 与可用Python版本；截取版本、当前目录、首次任务及新文件。已安装软件不重装补图。
2. A002：截取Codex任务、真实代码修改和运行：python3 ledger.py --input sample.csv。预期收入5000、支出62、结余4938。
3. A003：在第三章练习副本运行 python3 ledger.py --input sample.csv --output report.md，截取报告；再运行相同命令，截取拒绝覆盖。首次目标应不存在。
4. A004：在第四章练习副本运行 python3 -m unittest -v，截取真实结果。没有实际失败和修复就不制作前后对比。

截图命名建议 A001-01-version-macos.png 等。收到后核对、脱敏、另存处理版并嵌入。Windows命令未经本轮验证。
