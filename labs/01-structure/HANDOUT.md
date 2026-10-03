# Structure Lab · 整理师兄的草稿

## 情景

导师要看论文结构，但草稿用加粗文字冒充标题，摘要混在正文里，所有内容塞在 main.tex。你需要把它整理成可维护的工程。

## 启动

在项目根目录运行 `python tools/lab.py start 01`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 将草稿整理成标题、摘要、目录、引言、方法、结果与局限。用 section / subsection 表示层级，并给三个主要章节稳定标签。目录只显示到 subsection。

2. 将三个章节拆到 sections/intro.tex、sections/method.tex、sections/results.tex，通过 input 接入。子文件不能再有 documentclass 或 document 环境。添加指向 ../main.tex 的根文件注释。

3. 加入无序列表、有序列表和术语描述列表各一处。使用 emph 或 textbf 标记一个概念，用局部分组限制 small 的作用范围，并给数据来源加脚注。

4. 让 sensor_v2、20%、A&B 三段文字在 PDF 中正确显示。不要直接插入未转义的特殊字符。

5. 将方法和结果两节交换顺序，观察自动编号和目录，再恢复。另在副本中把 input 换为 include，记录分页变化。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 目录对应真实章节；三份子文件由唯一主文档调用。
- 字号改变不泄漏到后文，三个列表与特殊字符正确显示。
- 章节重排无需手改编号；用副本观察并解释 input 和 include 的分页差别。

## 技术检查

`python tools/lab.py check 01`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-01.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

新增一个“误差定义”小节并让目录自动更新，说明星号标题与普通标题的差别。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

先用注释画出导言区与正文边界，再拆文件。

</details>

<details><summary>提示 2</summary>

空行代表分段；连续空格不能可靠地排版对齐；字号声明放在一对大括号内。

</details>

<details><summary>提示 3</summary>

目录需要多轮编译。article 系列没有 chapter；短论文用 section，学位论文章结构见 Lab 06。

</details>

## 学习对应

配套讲稿：text-style.tex · structure.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/01-structure`，有完整可编译源码。
