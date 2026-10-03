# LaTeXLab · 科研论文排版自学工具

在 GitHub 点击 **Code → Download ZIP**，下载并解压整个仓库，或使用 `git clone https://github.com/Southwall-Tester/LeTeXLab.git`。

双击 **开始学习.html**。在自己习惯的 VS Code、TeXstudio、Overleaf 或其他 LaTeX 工具中修改工程，回到手册查看核验结果、回答理解题并检查 PDF。无需教师判关，也不需要提交给其他人。

任务采用起始工程、情景修改、故障定位和分级提示。可以使用智能体或表格生成器；练习重点是读懂、修改、调试并验证生成结果。

## 开始

1. 保留 `labs/` 中的起始题目，运行 `start` 或复制某关 `starter` 到自己的目录。每关可以独立开始。
2. 在所选编辑器中打开该关 `main.tex`，按任务修改并构建。工程带有局部 VS Code 配置；在线平台可上传 `downloads/` 中的对应压缩包。
3. 运行 `check`，打开本次报告，并把 `reports/latest-00.json` 导入离线手册。已有工程可通过 `--project` 指定路径。
4. 完成页面的两道理解题和两项 PDF 自查。在副本中先预测、再做变式操作，最后恢复自己的最终版本。

```text
python tools/lab.py doctor
python tools/lab.py start 00
python tools/lab.py check 00
python tools/lab.py check 03 --project "你的工程路径"
```

检查器会在 `_build/` 创建独立副本，使用本地 TeX 工具实际构建，保留 `check-report.json`、`check-report.html`、`ai-review-prompt.txt` 与日志；构建成功时保留本次 PDF。`reports/latest-XX.json` 是该关最近一次报告的导入入口。每项结果为 `pass`、`fail` 或 `unavailable`，整体状态为 `passed`、`needs_work` 或 `blocked`。缺少工具或证据不会显示成自动通过。检查器自身仅依赖 Python 标准库，PDF 取证另需 `pdftotext` 和 `pdfinfo`，可用 `doctor` 查看。

主关进度只采用 `check_scope='lab'` 的完整核验报告。运行 `build` 或编译支线后，重新运行该关主入口的 `check`，再导入更新后的报告。生成的 AI 请求含真实证据摘录；摘录可能截断，PDF 文本也不能代表视觉核对。

没有本地 TeX 时，可在在线平台修改、编译并下载真实源码、PDF 和日志，使用手册中的本关 AI 核验请求辅助检查，再记录结论与证据。此路线明确标为 AI 辅助核对。完整流程见 [自学与核验](docs/SELF-STUDY.md)。

## 目录

- `开始学习.html`：任务、提示、报告导入、理解题、PDF 自查与本机进度。
- `labs/00-boot` 至 `labs/07-submission`：任务书、可选自学记录模板和起始工程。
- `work/`：实际修改的工程，`start` 不覆盖已有内容。
- `downloads/`：可直接上传在线平台的各关起始包。
- `reports/`：各关最近一次本地核验报告。
- `_build/`：各次构建副本、真实输出、日志与核验报告。
- `selfstudy.json`：逐关理解题、PDF 自查项与 AI 核验请求。
- `instructor/solutions/`、`instructor/previews/`：供自学对照的参考实现与已构建 PDF；目录名沿用项目结构。
- `docs/`：自学流程、工具指南、知识映射、模板迁移和维护记录。
- `sources/`：视频和配套讲稿来源记录。未逐分钟播放核验，不提供猜测时间戳。

报告提供有限的技术证据，理解题和自查帮助发现遗漏，均不证明学习效果。源码、PDF、报告与个人记录由自己保留。

## 学习资料

- [从零开始使用 LaTeX 排版论文](https://www.bilibili.com/video/BV1Z24y157GM/)：知识映射依据该视频关联的 2023-04-01 配套讲稿，见 [知识覆盖](docs/COVERAGE.md)。
