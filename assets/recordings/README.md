# 四章 Codex CLI 动图与证据

使用 Hermes gif_codex 技能的事件重放流程制作。独立CLI真实执行，不访问桌面窗口；GIF重新计时、路径脱敏、长输出节选，完整错误保留。

|章节|动图|静态末帧|事件时间线|
|---|---|---|---|
|A001|[GIF](20261118T133012Z/A001/demo.gif)|[PNG](20261118T133012Z/A001/demo-last.png)|[时间线](20261118T133012Z/A001/timeline.md)|
|A002|[GIF](20261118T133012Z/A002/demo.gif)|[PNG](20261118T133012Z/A002/demo-last.png)|[时间线](20261118T133012Z/A002/timeline.md)|
|A003|[GIF](20261118T133012Z/A003/demo.gif)|[PNG](20261118T133012Z/A003/demo-last.png)|[时间线](20261118T133012Z/A003/timeline.md)|
|A004|[GIF](20261118T133012Z/A004/demo.gif)|[PNG](20261118T133012Z/A004/demo-last.png)|[时间线](20261118T133012Z/A004/timeline.md)|

独立验收：[verification.json](20261118T133012Z/verification.json)。四章进程退出码均为0；实际生成的8个unittest用例独立重跑通过。

制作工具：asciinema 3.2.1、agg 1.9.0；GIF均为1105×882。已查看首帧／末帧，中文正常。第1章内层版本命令的PATH别名权限警告保留，版本命令仍返回0；不是安装成功的证明。

原始未脱敏记录仅保存在Git忽略目录examples/work；公开副本进行路径脱敏。没有使用clean_cast删除错误。没有原生应用截图。代码许可和正文出版权仍待作者登记。
