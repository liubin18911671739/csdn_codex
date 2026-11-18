# Codex 应用实战

面向能安装软件、愿意使用少量命令的实用用户，筹备 CSDN 付费专栏。首季24篇，以 CLI 为主线、IDE 为配套入口，围绕编程、文件、文档、数据与研究任务交付可检查成果。

付费内容配套练习输入、任务指令、纠错过程和验收方法。A001 免费试读，其余为付费候选；专栏不包含模型订阅或第三方费用。价格、上线时间待确定，不自动发布。

## 进度与导航

现有 A001—A004 四篇草稿，均未达到 ready。A009、A042 当前正文缺失，保留编号待确认。Windows 为目标环境，当前 macOS 检查不替代 Windows 实测。

- [首季与后续目录](planning/catalog.md)
- [文章元数据](planning/articles.json)
- [产品与排期](planning/strategy.md)
- [待办](TODO.md)
- [个人文风卡](style/个人文风卡.md)
- [来源边界](sources/README.md)
- [发布清单](publishing/checklist.md)


## 前四篇图文重写稿

- [第1章：先交付环境记录](articles/001-start.md)
- [第2章：生成收支汇总工具](articles/002-setup.md)
- [第3章：分类汇总与报告保护](articles/003-task.md)
- [第4章：8项测试与交付验收](articles/004-review.md)

本版按真实末帧、GIF、代码与执行记录重写，图片放在对应步骤，保留提示词、Mermaid、排错与迁移练习。代码附件统一引用20261118T133012Z批次；早期示例不作为本版交付依据。四篇仍为draft，Windows与安装登录界面待验证。

## 维护

修改元数据后运行 `python3 scripts/index.py`，再运行 `python3 scripts/check.py`。检查覆盖顺序、资源、证据关联和本地链接，不代表完成技术验收。

按编号逐篇交付，不批量扩写整季。每篇先核官方来源，后起草，再分别完成事实与文风审查。ready 需有验证 Markdown 及同名 JSON，包含 article、technical_pass、sources_pass、environment、actual_outputs、source_checks；证据必须来自真实检查，字段通过不能代替人工审查。

历史目录保存在 planning/archive，原稿保存在 articles/archive。正文保留权利记录，代码独立标注许可；不得自动发布、签约、支付或静默覆盖原件。

本轮已扩写前四篇并添加 Mermaid 图；全项目按个人文风卡编辑。Windows、安装登录及IDE界面仍待验证；独立Codex CLI和GIF已完成验证，代码授权待作者确认。

前四章已改为安装→收支工具初版→报告扩展→测试交付。代码样例本机检查通过；正文仍需进一步扩写、减少重复，截图和平台验证待完成。

## 四章CLI动图批次 20261118T133012Z

已按Hermes gif_codex技能完成四次独立CLI任务、四份GIF及静态帧，事件重放明确标注。生成代码经独立验收，第4章8个测试通过。Windows与安装登录截图仍待验证，四篇保持draft。

## 第五章Flask网站

[文章](articles/005-flask.md)与[项目](examples/flask-ledger/README.md)已完成；19项测试及浏览器上传下载验证通过。本机运行地址http://127.0.0.1:5055/，尚未公网部署。
