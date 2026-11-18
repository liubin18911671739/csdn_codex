# 验证记录

2026-11-18，本机 Python unittest，未安装包，未启动 HTTP 长期服务。

1. 修改前：运行 `python3 -m unittest -v`，原有 8 项测试全部通过。
2. 提取公共逻辑后：原有 8 项测试全部通过，`test_ledger.py` 未修改。
3. 首次完整运行：19 项测试，11 个子用例失败。失败均来自 `test_invalid_records` 中 `assertNotIn('收支概览', response.text)`：错误页上传按钮也含“生成收支概览”，导致误判。静态文件测试另有未关闭响应的 ResourceWarning。此为真实失败记录，非预设失败。
4. 修复：断言检查结果卡片的 `aria-label="收支概览"`；静态文件响应使用上下文管理器关闭。上传请求使用 BytesIO，避免默认 multipart 临时文件缓冲。
5. 最终完整测试输出见 `test-results.txt`，包含原有 8 项 CLI 测试及新增 11 项网页测试。

测试通过 Flask 测试客户端检查服务器输出与转义。未使用浏览器做视觉验收或执行 Blob 下载；Windows 未实测。README 和实现已核对路由、编码、大小限制、错误状态码及运行命令。本次是代码练习交付，不修改专栏文章元数据或发布状态。
