# 维护与复现

学习者只需编辑器与 TeX 环境；可选的检查器只依赖 Python 3.9+ 标准库。以下依赖和命令仅用于重新生成课程材料或维护检查。

生成课程需要 matplotlib；生成离线手册需要 Python-Markdown；PDF 渲染检查使用 PyMuPDF/Pillow；网页集成检查使用 Playwright 和本机 Edge。这些不构成学习者的额外安装要求。

```text
python tools/build_course.py
python tools/build_handbook.py
python tools/validate_course.py
python tools/validate_targeted.py
python -m unittest discover -s tools -p test_selfcheck.py
python tools/test_handbook.py
python tools/finalize.py
```

build_course 会覆盖 labs/ 与 instructor/solutions/ 的生成文件；不会修改 work/。先在生成器中修改，再生成；学习者修改始终留在 work/ 或自己的目录。

如需只验证变动关卡，可用 `validate_course.py --labs 03 04`。源码包按项目相对路径组织，不包含绝对机器路径、临时编译缓存或学习者工作目录。

参考解只是可行解。检查器读取实际编译文件、日志、交叉引用、文献输出及 PDF 文本，部分源码规则仍采用有限的特征匹配；无法可靠判定的写法应标为未能核验，结合日志、源码与 PDF 复核。检查规则应支持等效的合法写法。新增任务须同步起始工程、参考解、HANDOUT、覆盖矩阵、selfstudy.json 与核验规则。

validate_course 在各验证构建目录生成真实报告，不写入学习者的 reports/latest-XX.json。网页测试从这些验证目录读取参考报告，测试前先运行 validate_course；参考通过记录不代表学习者已完成任务。课程打包排除 work/、reports/ 与临时构建目录。

离线手册将 selfstudy.json 中的理解题、PDF 自查项和 AI 核验请求嵌入 HTML。改动任务时同步检查这些内容；报告导入与 AI 辅助记录使用不同状态，不应把模型认可写成自动通过。打包时保留 selfstudy.json 与 docs/SELF-STUDY.md。
