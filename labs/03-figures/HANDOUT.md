# Figure Lab · 审稿人看不清你的图

## 情景

审稿意见：“两张图无法比较，图题缺失，正文只说见下图。换成双栏后更是溢出版心。”图已经由组内脚本生成，你负责可靠地排进去。

## 启动

在项目根目录运行 `python tools/lab.py start 03`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 用 figures/baseline.pdf 和 calibrated.pdf 替换占位图。采用相对路径或 graphicspath；不要使用自己的桌面绝对路径。

2. 把两图排为一张总图下的 (a)(b) 两个子图，各约 0.48 倍当前 linewidth，保留纵横比。加入子图题、总图题、稳定标签，并在正文引用总图及两个子图。

3. 总图说明“教学合成数据”。图在正文首次提及附近浮动，理解 [htbp] 是位置偏好。对比 h 与 H：H 需要 float 宏包，可能造成空白，不能把它当普遍修复。

4. 在副本中将 documentclass 加 twocolumn，确认当前栏内图片不溢出；解释嵌套 minipage 中 linewidth 和 textwidth 的差别。

5. 再在副本中把 subfigure 换为两个 minipage，各自 caption，观察“一个图的两个子图”和“两张独立编号的图”的区别，保留对比 PDF 或截图。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- 两幅真实素材均出现，比例不变，标签在 caption 后，正文使用 ref。
- 单栏和双栏试验都无图片越界；文件夹搬家后仍可编译。
- 通过副本变化解释浮动体、相对尺寸和两种并排编号方式。

## 技术检查

`python tools/lab.py check 03`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-03.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

交换两子图顺序，并把每幅宽度调为 0.44 倍 linewidth；引用仍应跟随对象。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

先插入一张图并成功编译，再建立子图结构。

</details>

<details><summary>提示 2</summary>

graphicx 负责插图，subcaption 提供 subfigure；每个子图内部用 width=linewidth。

</details>

<details><summary>提示 3</summary>

总标签放在总 caption 之后；子标签放在各自 caption 之后。不要用图 1(a) 这样的正文常量。

</details>

## 学习对应

配套讲稿：figure.tex · reference.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/03-figures`，有完整可编译源码。
