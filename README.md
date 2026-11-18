# 用 AI 完成真实工作

面向愿意学习少量命令行的 Windows 办公、研究与创作用户，筹备 CSDN 付费专栏及后续书稿。教程围绕真实任务、明确输入和可检查输出组织。

## 当前进度

截至 2026年11月18日，以 [文章元数据](planning/articles.json) 为准：15 个单元、60 篇选题，其中 3 篇 draft、57 篇 planned，暂无 ready 文章。

已有草稿为 [A001 入门](articles/001-start.md)、[A009 文件整理](articles/009-files.md)、[A042 LibreOffice 迁移](articles/042-libreoffice.md)。历史稿保留在 `articles/archive/`，不计作新增文章。

当前编写环境为 macOS，三篇草稿均待 Windows 实测，尚未采集截图。[验证记录](planning/validation.md)记载了文件整理脚本在本机 Python 3.12 合成数据上的检查，该结果不替代 Windows 验证。

下一步先修订 A001，再按编号推进 A002、A003。具体问题、优先级及验收标准见 [TODO](TODO.md)。

## 仓库导航

| 位置 | 用途 |
|---|---|
| [AGENTS.md](AGENTS.md) | 项目写作与操作规范 |
| [planning/](planning/catalog.md) | 文章元数据、完整目录、排期与审查记录 |
| [articles/](articles/001-start.md) | 当前文章草稿；archive 保存历史版本 |
| [style/](style/个人文风卡.md) | 个人文风卡，当前仅由两篇样本支持 |
| [sources/](sources/README.md) | 来源与能力映射；工具、技能清单为会话快照 |
| [templates/](templates/article.md) | 文章、验证与勘误模板 |
| [examples/](examples/organize.py) | 随文可运行代码 |
| [assets/](assets/README.md) | 截图及素材权利登记 |
| scripts/ | 结构检查与目录生成脚本 |
| [publishing/](publishing/checklist.md) | 专栏介绍及人工发布清单 |
| [book/](book/outline.md) | 后续成书路线 |

## 常用命令

在项目根目录使用 Python 3，以下脚本仅使用标准库：

```sh
python3 scripts/check.py
```

检查文章数量、部分必填元数据、资源文件与 Markdown 本地链接。目前脚本固定要求 3 篇 draft；推进文章状态前需处理这一限制。检查通过不等于教程完成技术验收，也不验证外部链接或账号权限。

修改文章元数据后运行：

```sh
python3 scripts/index.py
```

此命令会根据 `planning/articles.json` 重写 `planning/catalog.md`，不要在生成目录中单独维护选题信息。以上命令在本机检查，不作为 Windows 实测记录；Windows 使用已确认可用的 Python 启动命令。

文件整理示例默认只预览，加 `--apply` 才复制，目标目录已存在则拒绝执行。完整练习与验收步骤见 A009。

## 逐篇交付流程

1. 按元数据编号推进，先修订 A001，再新写 A002、A003 等；到 A009、A042 时修订已有稿，不重复建稿。
2. 先读个人文风卡，明确任务、输入和验收输出，再查官方技术来源。会话私有工具名不能写作公开 API。
3. 使用文章模板起草，分别完成事实审查与文风审查；文风通过不替代技术验收。
4. 按[验证模板](templates/validation.md)记录环境、版本、输入、实际输出、失败与恢复、截图及未验证项。Windows 操作未经实测必须注明。
5. 每次交稿同步文章元数据、验证记录及生成目录。只有测试和来源检查完成后才能改为 ready。
6. 发布前执行人工发布清单，由作者人工提交并登记 URL、价格及版本。

`planned` 表示已列入选题，`draft` 表示已有草稿，`ready` 表示已满足交付检查要求；ready 不代表已经发布。不得编造截图、测试结果、引用或账号权限。

## 权利、成本与发布边界

正文保留出版权记录，代码独立标注许可；截图和外部素材登记作者、来源、许可及出版使用范围。当前代码许可与逐篇权利记录仍待补齐，不能据仓库可读推断授权范围。

批处理默认预览，不得静默覆盖或删除原文件。不自动发布、签约或提交支付。平台资格、价格、协议、AI 声明与出版授权在上线前核实；[商业与排期](planning/strategy.md)中的价格和时间均为内部规划。

模型订阅、API、云算力及素材费用另行核对。来源中的会话快照不代表公共接口文档、服务登录状态或订阅权益承诺。
# csdn_codex
