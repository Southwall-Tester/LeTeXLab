# Submission Lab · 今晚交稿

## 情景

今天 20:00 截稿。你拿到一份可编译但不合格的合并稿，需要落实审稿意见，并让同事在另一台机器上得到同样的 PDF。

## 启动

在项目根目录运行 `python tools/lab.py start 07`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 从本关 starter 或自己的 Lab 06 结果开始。逐项落实 REVIEW.md：整理真实章节、修公式、补双子图、改三线表、导入三条文献、开启匿名模板。

2. 保留 sections/ 下独立章节；在正文动态引用公式、图、表及章节。删除过度科研结论，声明教学合成数据。在自己的记录中区分智能体/生成器产出与已经核对的部分。

3. 使用干净构建检查首个错误、引用、文献、浮动体、越界、中文缺字和残留 TODO。打开最终 PDF，逐页检查而非只看构建状态。

4. 整理源码包：main.tex、sections、figures、data、references.bib、labpaper.cls、README-BUILD.txt、REPORT.md。用 pack 命令或手动压缩，将源码包与最终 PDF 一起保留。

5. 把包解压到一个新目录，从 main.tex 重新编译，记录环境和结果。执行本关变式测试，保存变式前后证据，再恢复最终版。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 最终 PDF 包含摘要、引言、方法、结果与局限、正确公式、双子图、三线表、三条文献。
- 全部交叉引用和文献引用已解析，无报错和任务造成的越界。
- 解压后的源码不依赖原路径，能够重新构建；保留本次核验报告和自己的 PDF 自查记录。

## 技术检查

`python tools/lab.py check 07`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-07.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

审稿人临时要求交换结果与方法、先引用 Einstein、把双子图改成独立编号。完成变式，展示编号自动变化，然后恢复投稿要求。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

把审稿意见变成可观察输出，按“能编译→内容正确→格式正确→可移交”的顺序处理。

</details>

<details><summary>提示 2</summary>

不要逐处修正文中的“图 1”；改用 label/ref 让重排自然更新。

</details>

<details><summary>提示 3</summary>

check 只能证明部分技术条件，不会替你判断公式含义、版式美观、匿名完整性或科研结论。

</details>

## 学习对应

配套讲稿：综合自测 · 五项学习能力要求。精确视频时间点未核验。

参考实现在 `instructor/solutions/07-submission`，有完整可编译源码。
