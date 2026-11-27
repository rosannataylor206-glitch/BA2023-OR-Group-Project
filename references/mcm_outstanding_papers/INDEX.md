# MCM/ICM Outstanding论文参考库

建立日期：2026-11-28（北京时间）。用途：BA2023月球基地Report的研究表达、运筹优化写作与科学制图学习。**仅本地研读；本轮未上传GitHub。**

## 使用入口

- [逐篇分析与横向比较](PAPER_REVIEW.md)
- [论文写作规范](WRITING_GUIDELINES.md)
- [可视化与排版规范](VISUALIZATION_GUIDELINES.md)
- [当前OR Report重构方案](REPORT_RESTRUCTURE_PLAN.md)
- [来源、访问限制与2026检索记录](SOURCE_AND_ACCESS.md)
- [构建与保全检查](BUILD_REPORT.md)

## 收录与验证范围

五类目标赛题共26支官方O奖队伍，已全部收录每队一个可读主副本，共657物理页。另保留两份有缺陷的初次镜像作为来源差异记录，不计为新增论文。官方名单核实的是队伍/年份/题号/奖项；第三方PDF不是经认证的原提交全文，尤其注意下表副本差异。

[来源与SHA-256清单](_provenance/manifest.json)记录固定Git树/路径、下载链接、文件大小、哈希及渲染页码。[奖项证据](_provenance/award_verification.json)逐队保存COMAP对应题目的Outstanding段落条目；官方HTML和结果PDF保留在同目录。解析失败、文本缺层与正文错误不以文件名代替核验。

全文已逐页提取用于检索，研读采用章节定向阅读及逐篇代表页目视检查；不是657页逐行校勘、独立数学证明或算法复现。`_reading/队号/`含原始文本层、章节候选、全页缩略图、实际目视的detail/supplement/extra页面。缩略图仅导航；读过的高分辨率物理页由manifest逐篇列出。

## 按年份及题号导航

### 2025 MCM B — Managing Sustainable Tourism

[COMAP官方名单](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2025/results/)；本组7篇均为Outstanding Winner（已核实）。

- **2501687 — [Economy, Ecology, and Social Welfare: A Win-Win Approach for Sustainable Tourism in Juneau](2025/MCM_B/2501687.pdf)**，25页，4.23 MiB。
  来源：[下载页](https://github.com/xianDE1234561/American-Mathematical-Modeling-Competition-Preparation/blob/911a53e1435737fd9ea2d1751b2d6c5134a20c33/%E5%8E%86%E5%B9%B4%E5%AE%98%E6%96%B9%E8%B5%84%E6%96%99_2021-2025/2025/%E8%8E%B7%E5%A5%96%E8%AE%BA%E6%96%87_%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E5%BA%93/B%E9%A2%98/2025_B_O%E5%A5%96_2501687.pdf)；[研读卡](PAPER_REVIEW.md#team-2501687)。
  核心方法：CVM货币化；多目标非线性规划；PSO；情景比较。参考价值：借鉴推荐方案说明“何时、多少、用于什么”，不引入CVM替代现有成本模型。
- **2502617 — [Overload Alarm: Pareto Optimization of the Economic-Social-Environmental Triangle](2025/MCM_B/2502617.pdf)**，26页，4.93 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2025%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/B/2502617.pdf)；[研读卡](PAPER_REVIEW.md#team-2502617)。
  核心方法：成本效益；福利/生态承载；加权非线性优化；SLSQP。参考价值：借鉴目标/权重/约束同页呈现；本项目保留有限目录证据范围。
  副本备注：摘要文本层为空，队号已通过渲染p1目视确认。
- **2503268 — [Rebalancing Nature’s Scale: A Model to Tame Overtourism](2025/MCM_B/2503268.pdf)**，26页，13.72 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2025%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/B/2503268.pdf)；[研读卡](PAPER_REVIEW.md#team-2503268)。
  核心方法：旅游ODE；Lotka–Volterra/Logistic/SIS启发；AHP；Morris。参考价值：借鉴有限策略集、基准对照与参数估计诚实披露。
- **2504448 — [Sustainable Tourism Management in Juneau](2025/MCM_B/2504448.pdf)**，25页，3.81 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2025%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/B/2504448.pdf)；[研读卡](PAPER_REVIEW.md#team-2504448)。
  核心方法：需求递推；经济/环境/满意度；动态规划；熵权。参考价值：借鉴明确递推与预算反馈，但本项目无需新建动态规划。
- **2505199 — [Breaking through the Tourism Dilemmas in Juneau: The Road to Sustainable Development Driven by a Multi-objective Model](2025/MCM_B/2505199.pdf)**，28页，3.84 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2025%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/B/2505199.pdf)；[研读卡](PAPER_REVIEW.md#team-2505199)。
  核心方法：多目标非线性优化；NSGA-II；拟合；多参数情景。参考价值：作为反例提醒本项目信件、摘要、预算表必须同源。
- **2509557 — [The Triangular Balance of Environment, Economy, and Society: A System Dynamics-Based Model for Sustainable Tourism Management](2025/MCM_B/2509557.pdf)**，26页，7.02 MiB。
  来源：[下载页](https://github.com/xianDE1234561/American-Mathematical-Modeling-Competition-Preparation/blob/911a53e1435737fd9ea2d1751b2d6c5134a20c33/%E5%8E%86%E5%B9%B4%E5%AE%98%E6%96%B9%E8%B5%84%E6%96%99_2021-2025/2025/%E8%8E%B7%E5%A5%96%E8%AE%BA%E6%96%87_%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E5%BA%93/B%E9%A2%98/2025_B_O%E5%A5%96_2509557.pdf)；[研读卡](PAPER_REVIEW.md#team-2509557)。
  核心方法：系统动力学；非线性反馈；L-BFGS-B；情景与迁移。参考价值：借鉴参数溯源表与参数组合的管理解释，不导入旅游ODE。
- **2517929 — [From TBMP to TSMP: Juneau’s Tourism Never Ends](2025/MCM_B/2517929.pdf)**，25页，4.57 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2025%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/B/2517929.pdf)；[研读卡](PAPER_REVIEW.md#team-2517929)。
  核心方法：多目标NSGA-II；回归/AHP；支出反馈；局部扰动。参考价值：借鉴边界解→管理瓶颈的讨论，避免本项目无依据增添算法。

### 2024 MCM B — Searching for Submersibles

[COMAP官方名单](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2024/results/)；本组4篇均为Outstanding Winner（已核实）。

- **2407038 — [Unlocking the Abyss: A Dynamical Model for Deep-Sea Adventure Safety and Rescue Strategies](2024/MCM_B/2407038_reformship.pdf)**，25页，3.54 MiB。
  来源：[下载页](https://reformship.github.io/pages/3competition/4mcm/MCM%20Outstanding/2024/B/2407038.pdf)；[研读卡](PAPER_REVIEW.md#team-2407038)。
  核心方法：ARIMA/岭回归；动力学；GA装备权衡；Bayes栅格搜索。参考价值：借鉴“预测/机理计算→资源配置→服务效果”的单条证据链。
  副本备注：原GitHub副本文字重叠；另用reformship副本。
- **2411570 — [From Lost to Found: Roam in the Ionian Sea](2024/MCM_B/2411570_reformship.pdf)**，25页，16.16 MiB。
  来源：[下载页](https://reformship.github.io/pages/3competition/4mcm/MCM%20Outstanding/2024/B/2411570.pdf)；[研读卡](PAPER_REVIEW.md#team-2411570)。
  核心方法：微分动力学；EWM-TOPSIS；Monte Carlo；改进圆形搜索。参考价值：借鉴物理单位表与变量初值说明，避免摘要只有方法名。
  副本备注：原GitHub下载副本解析为0页；另用reformship副本。
- **2419984 — [Time is Life: Precise Localization and Faster Search](2024/MCM_B/2419984.pdf)**，25页，12.43 MiB。
  来源：[下载页](https://github.com/xianDE1234561/American-Mathematical-Modeling-Competition-Preparation/blob/911a53e1435737fd9ea2d1751b2d6c5134a20c33/%E5%8E%86%E5%B9%B4%E5%AE%98%E6%96%B9%E8%B5%84%E6%96%99_2021-2025/2024/%E8%8E%B7%E5%A5%96%E8%AE%BA%E6%96%87_%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E5%BA%93/B%E9%A2%98/2024_B_O%E5%A5%96_2419984.pdf)；[研读卡](PAPER_REVIEW.md#team-2419984)。
  核心方法：RK4；动力学；熵权成本效益；Monte Carlo；ACO/Bayes。参考价值：借鉴Q2故障→结果变化→为何应采取动作，而非只列故障因子。
- **2425792 — [Save the Submersible: An Combined Method of Computational Fluid Dynamics and Kalman Filter](2024/MCM_B/2425792.pdf)**，25页，10.15 MiB。
  来源：[下载页](https://github.com/xianDE1234561/American-Mathematical-Modeling-Competition-Preparation/blob/911a53e1435737fd9ea2d1751b2d6c5134a20c33/%E5%8E%86%E5%B9%B4%E5%AE%98%E6%96%B9%E8%B5%84%E6%96%99_2021-2025/2024/%E8%8E%B7%E5%A5%96%E8%AE%BA%E6%96%87_%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E5%BA%93/B%E9%A2%98/2024_B_O%E5%A5%96_2425792.pdf)；[研读卡](PAPER_REVIEW.md#team-2425792)。
  核心方法：简化6DOF；Kalman Filter；PCA；Voronoi。参考价值：借鉴明确数学条件与误差量定义；不将本项目确定性证书写成统计置信。

### 2024 ICM D — Great Lakes Water Problem

[COMAP官方名单](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2024/results/)；本组4篇均为Outstanding Winner（已核实）。

- **2417004 — [Regulating the Water of Tomorrow: A Multi-Layer Optimization Model for the Great Lakes](2024/ICM_D/2417004.pdf)**，25页，8.73 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2024%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/D/2417004.pdf)；[研读卡](PAPER_REVIEW.md#team-2417004)。
  核心方法：网络水流；进阶气象模型；NSGA-II；多元回归。参考价值：借鉴基础模型→已有扩展的叙述，不为版式而新增复杂模型。
- **2417831 — [Harmony of the Great Lakes: A Water Level Balance Approach](2024/ICM_D/2417831.pdf)**，25页，12.57 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2024%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/D/2417831.pdf)；[研读卡](PAPER_REVIEW.md#team-2417831)。
  核心方法：GA/AHP利益目标；湖链水动力；预测反馈控制。参考价值：借鉴“评价标准→可行执行策略→情景后果”的章节衔接。
- **2419588 — [Optimizing Great Lakes Water Management: An Adaptive Hydrological Network Approach](2024/ICM_D/2419588.pdf)**，27页，2.98 MiB。
  来源：[下载页](https://github.com/BohanSu/MCM-ICM/blob/a643f07c5312823a166dd821acb6fabf6edb412b/O%E5%A5%96%E6%96%87%E7%AB%A0/2024%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96/D/2419588.pdf)；[研读卡](PAPER_REVIEW.md#team-2419588)。
  核心方法：水文网络；利益满意度ESS；MPC。参考价值：借鉴“具体省略→受影响决策→需要怎样验证”的局限写法。
  副本备注：封面题号C与官方2024 D身份不一致。
- **2429211 — [Dynamic Dams Model: A Multigranular, Human-Centered Approach For Modeling Water In The Great Lakes](2024/ICM_D/2429211.pdf)**，25页，3.05 MiB。
  来源：[下载页](https://github.com/xianDE1234561/American-Mathematical-Modeling-Competition-Preparation/blob/911a53e1435737fd9ea2d1751b2d6c5134a20c33/%E5%8E%86%E5%B9%B4%E5%AE%98%E6%96%B9%E8%B5%84%E6%96%99_2021-2025/2024/%E8%8E%B7%E5%A5%96%E8%AE%BA%E6%96%87_%E5%85%AC%E5%BC%80%E8%B5%84%E6%96%99%E5%BA%93/D%E9%A2%98/2024_D_O%E5%A5%96_2429211.pdf)；[研读卡](PAPER_REVIEW.md#team-2429211)。
  核心方法：动态流网络；宏/微两层LP；时滞相关；线性回归。参考价值：首选：借鉴本项目运输与入住两阶段、有限候选优化的清晰表达。

### 2022 MCM B — Water and Hydroelectric Power Sharing

[COMAP官方名单](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2022/results/)；本组6篇均为Outstanding Winner（已核实）。

- **2200084 — [A Model for Better Use of Water Resources Based on Marginal Utility and Auction Theory](2022/MCM_B/2200084.pdf)**，24页，4.63 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2200084.pdf)；[研读卡](PAPER_REVIEW.md#team-2200084)。
  核心方法：时变LP；资源网络；边际效用；独立私人价值拍卖。参考价值：借鉴建设期→入住期资源网络及停止/失效条件的写法。
- **2202748 — [Salvation in an Age of Water Scarcity](2022/MCM_B/2202748.pdf)**，25页，1.54 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2202748.pdf)；[研读卡](PAPER_REVIEW.md#team-2202748)。
  核心方法：运输模型；多目标规划；维持时间迭代；墨西哥分配。参考价值：借鉴水量守恒、处理能力与供应时间的分层解释。
- **2207864 — [Water and Hydroelectric Power Sharing](2022/MCM_B/2207864.pdf)**，25页，1.73 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2207864.pdf)；[研读卡](PAPER_REVIEW.md#team-2207864)。
  核心方法：等效库形；多目标调度；阶段划分；EWM-TOPSIS；0–1规划。参考价值：借鉴预置、在建、入住阶段的阈值规则，不迁移水库模型。
- **2211922 — [Reservoir Management: The Art of Proper Allocation](2022/MCM_B/2211922.pdf)**，25页，2.51 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2211922.pdf)；[研读卡](PAPER_REVIEW.md#team-2211922)。
  核心方法：双库差分系统；多目标GA；PCA优先分配。参考价值：借鉴主文保留关键推导、长证明进入附录的分层。
  副本备注：封面年份2021与官方2022 B身份不一致。
- **2213970 — [Decision System for Optimizing Water Allocation](2022/MCM_B/2213970.pdf)**，25页，2.15 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2213970.pdf)；[研读卡](PAPER_REVIEW.md#team-2213970)。
  核心方法：非线性规划/模拟退火；博弈/Newton；短缺指标迭代。参考价值：借鉴本项目有限目录最优、闭式界与LP复核范围的准确措辞。
- **2228168 — [A Two-Stage Water Resource Optimal Operation Model Based on Genetic Algorithm](2022/MCM_B/2228168.pdf)**，25页，1.40 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2022/B/2228168.pdf)；[研读卡](PAPER_REVIEW.md#team-2228168)。
  核心方法：LP运输；两阶段规划；精英GA；差分进化。参考价值：借鉴本项目变量→约束→证书→结果的技术表达。

### 2021 MCM B — Fighting Wildfires

[COMAP官方名单](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2021/results/)；本组5篇均为Outstanding Winner（已核实）。

- **2102199 — [Build an Army of Drones to Fight Wildfires](2021/MCM_B/2102199.pdf)**，25页，3.18 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2021/B/2102199.pdf)；[研读卡](PAPER_REVIEW.md#team-2102199)。
  核心方法：栅格多目标优化；Poisson极端事件；Tabu Search。参考价值：借鉴Q2故障输入→服务能力→预算影响的表达。
- **2104673 — [‘Rapid Bushfire Response’ UAV System](2021/MCM_B/2104673.pdf)**，25页，2.16 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2021/B/2104673.pdf)；[研读卡](PAPER_REVIEW.md#team-2104673)。
  核心方法：区域离散优化；元胞自动机；地形通信约束。参考价值：借鉴Report结尾“建议+条件+采购/执行依据”。
- **2105363 — [Rapid Bushfire Response for Emergency Response](2021/MCM_B/2105363.pdf)**，25页，4.08 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2021/B/2105363.pdf)；[研读卡](PAPER_REVIEW.md#team-2105363)。
  核心方法：风险分区；数量与成本优化；贪心混合；信号损失。参考价值：借鉴设备/电力/库存计量的正文解释，避免只贴JSON。
- **2116496 — [Drone System VS Wildfire](2021/MCM_B/2116496.pdf)**，25页，2.63 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2021/B/2116496.pdf)；[研读卡](PAPER_REVIEW.md#team-2116496)。
  核心方法：GMM；K-means；最小生成树；AHP/TOPSIS；灰色预测。参考价值：借鉴把成本与安全的取舍写成可解释推荐。
- **2127300 — [Rapid Bushfire Response System](2021/MCM_B/2127300.pdf)**，25页，1.98 MiB。
  来源：[下载页](https://github.com/YuchenHuang2006/MCM-ICM-Outstanding-Papers/blob/2661db06596e0e02f4094156005bb7caecd227fe/2021/B/2127300.pdf)；[研读卡](PAPER_REVIEW.md#team-2127300)。
  核心方法：遗传算法；LSTM；无线传播损失；地形优化。参考价值：借鉴基础/故障追加成本分表；警惕模板页眉与身份残留。
  副本备注：p24–25页眉队号2120188与主体2127300不同，附件身份待核。

## 2026 MCM B — Creating a Moon Colony Using a Space Elevator System

官方已确认6支O奖队伍：2600475、2602524、2605749、2621057、2624189、2625185。[COMAP结果](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/results/)与[官方论文入口](https://www.comap.org/membership/member-resources/item/creating-a-moon-colony-using-a-space-elevator-system)。

本轮未找到可确认的免费、无访问限制全文渠道；未取得这6篇PDF，题名、方法与结论均**尚未研读/尚未验证**。官方页面明确Student Papers (6)须Mathmodels会员，未购买、未借用账号、未绕过限制。详情见[2026待获取清单](2026/MCM_B/AVAILABILITY.md)。

## 权利和学术使用

来源仓库公开可访问，不代表论文版权转移或允许Public再分发。保留水印、署名、原始PDF；不把参考文献整表复制到本项目，不以获奖替代正确性验证。学习结构、图表的论证功能与数学解释方法；不抄用文字、模型参数、数据、结论或图片。本库`.gitignore`阻止PDF、页面图像及全文文本层被普通暂存；不得用force-add绕过。两位作者可本地阅读或访问来源链接，远程再分发需另核权利。
