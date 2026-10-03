# Results Lab · 让公式和表格对得上

## 情景

智能体生成的公式能编译，但计算的其实不是 RMSE；表里还抄错了一个结果。你需要核对含义，再按论文规范排版。

## 启动

在项目根目录运行 `python tools/lab.py start 04`，或手动复制本关 `starter` 文件夹和 `REPORT.md` 到自己的工作目录。打开复制品中的 `main.tex`。每关独立可做，不会因上一关卡住而无法开始。

## 任务

1. 阅读 data/observations.csv。修正 RMSE 为平方误差均值再开平方；写清 n、真实值、预测值与单位。独立计算两方法的 RMSE 和 MAE，保留三位小数。

2. 使用带编号 equation 并由 eqref 引用；用 align 排两行误差定义，增加一个无编号分段函数及一个矩阵。禁止用图片替代数学公式。

3. 将 data/summary.csv 导入 Tables Generator 或用智能体生成表格草稿，再核对原始数据。用 booktabs 三线表、合并表头、caption 和 label；无竖线，数字右对齐。表上方标题、正文动态引用。

4. 表格结果应与原始数据一致。把“降低 50%”限制为本教学样本上的观察，不推断真实有效性。

5. 在 scratch.tex 副本中试一次固定宽度 p 列、multicolumn 表头以及 gather / multline。读扩展卡选择 longtable 或 threeparttable 处理给定场景。

## 结果对照

将源码、最终 PDF 和核验报告留给自己。REPORT.md 是可选笔记；下面这些结果可结合自动报告、理解题与 PDF 自查逐项核对。

- RMSE 公式含平方、均值与平方根，MAE 含绝对值；两方法结果分别为 1.000 / 0.500。
- 表中名称、单位、列数与 CSV 一致，数字未被生成工具改写。
- 公式和表格均可引用；对齐与多行环境使用正确。

## 技术检查

`python tools/lab.py check 04`

检查器在 `_build/` 的副本中真实构建，生成 `check-report.json`、`check-report.html` 与日志，并更新 `reports/latest-04.json`。把 JSON 导入离线手册查看具体的 pass / fail / unavailable 项，再完成该关理解题和 PDF 自查。没有本地环境时，下载在线平台的当前源码、PDF 和日志，使用页面的本关 AI 核验请求并记录具体证据；此路线不会显示为自动通过。详见 `docs/SELF-STUDY.md`。

## 变式自测

仅在数据副本中将 Calibrated 第一个预测值改为 22，重新算指标并更新表；说明只改 LaTeX 公式为何不会自动重算静态表。

可以继续使用智能体。先预测，再在副本中修改并核对实际输出；完成后恢复最终版本。

## 按需提示

<details><summary>提示 1</summary>

本题合成数据的 Baseline 误差绝对值均为 1，Calibrated 均为 0.5。

</details>

<details><summary>提示 2</summary>

amsmath 提供 align、cases、pmatrix 和 eqref；不要把 align 套进 equation。

</details>

<details><summary>提示 3</summary>

三列每个普通数据行应有两个 &。检查平方根包住的范围，不能以编译成功判断数学正确。

</details>

## 学习对应

配套讲稿：math.tex · table.tex。精确视频时间点未核验。

参考实现在 `instructor/solutions/04-results`，有完整可编译源码。
