# Citation Lab · 文献编号大洗牌

## 情景

本次修改需要让编号按首次引用顺序出现，并补入一篇参考资料。你收到文献管理器导出的 .bib，却发现 [1] 不对应自己预期的那篇。

## 启动

在项目根目录运行 `python tools/lab.py start 05`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 阅读 references.bib 和 incoming.bib 的主键及字段。将 incoming.bib 的 lamport1994 合并到 references.bib，保留另两条记录；不手写正文参考文献列表。

2. 按正文首次引用顺序引用 lamport1994、knuth1984、einstein1905。设 biblatex 的 backend=biber、style=numeric、sorting=none，输出参考文献表。

3. 完整运行 XeLaTeX → Biber → XeLaTeX → XeLaTeX，或用 latexmk。说明 .bib、.bcf、.bbl、.aux 分别处在哪条链路。找出最初 undefined citation 的原因。

4. 交换正文前两处引用，重编译并记录 [1] 对象如何变化。不要靠修改 .bib 条目排列或手写 [1] 调编号。

5. 在副本中改用 authoryear 并比较显示；再编译 legacy/main.tex，识别 natbib + BibTeX 的另一套链路。不要在同一主文件同时加载 natbib 和 biblatex。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 三条文献都有合法主键且显示在文献表，无未定义引用。
- 主交付为数字引用且首次出现的 Lamport 对应 [1]；顺序变化有记录。
- 能指出不同模板的后端与样式入口；检查原始来源而非相信智能体编造条目。

## 技术检查

`python tools/lab.py check 05`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-05.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

把正文主键临时改错一个字母，区分缺条目、漏跑 Biber 与旧中间文件，再恢复。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

cite 的参数是 .bib 第一行的主键，不是标题、文件名或显示编号。

</details>

<details><summary>提示 2</summary>

sorting=none 按引用顺序；style 控制展示。Biber 读 .bcf，BibTeX 读 .aux。

</details>

<details><summary>提示 3</summary>

导入并不会自动引用全部文献；只有被引用的通常才输出。真实项目用 Zotero/JabRef/出版商导出，并对照来源核验元数据。

</details>

## 学习对应

配套讲稿：reference.tex · sjtuthesis.tex「参考文献」。精确视频时间点未核验。

参考实现在 `instructor/solutions/05-citations`，有完整可编译源码。
