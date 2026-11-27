# 优秀论文逐篇研读与横向比较

2026-11-28。身份核验与全文来源见[INDEX](INDEX.md)。以下均为本次分析，未继承旧手册的“已读”状态。页码统一指PDF**物理页**，可能与页眉、目录差1–2页；缺陷副本记录不能据此归责于原参赛者。

## 研读方法与适用范围

26篇均核对Summary页队号，检索全页文本层、章节和题注，结合逐篇高分辨率页面检查。每卡给出实际目视页码；文本层为空时通过渲染阅读，未把空文本判为缺章节。每篇的研究主线、模型表述、结果、敏感性、局限及面向决策者的附页分别分析。未复现这些论文的程序、核实所有引用或证明每条公式；文中的结果只用作“作者怎样呈现证据”的案例，不作为本项目数值依据。

## 推荐阅读顺序

1. **2429211**：OR主文首选，宏/微调度、目标与约束、情景与管理洞见。
2. **2211922、2202748**：资源守恒、网络/差分表达及技术正文与公众文章的分工。
3. **2419984、2407038**：多模型接口、数值方法与决策输出的连接。
4. **2509557、2503268**：参数来源、交互敏感性、基准比较。
5. **2116496、2104673**：把装备/配置/预算转为可执行建议。

这是对当前Report的适配判断，不是重新给获奖论文排序。

## 横向比较与可迁移判断

| 比较维度 | 本库的具体证据 | 对月球基地报告的含义 |
| --- | --- | --- |
| 研究主线 | 2429211分宏观目标/微观执行；2419984由定位接搜索；2503268由动力接有限策略评分 | “运输服务→建设→预置→入住保障→成本/环境决策”，每个箭头写清传入量 |
| 模型呈现 | 2228168按需求、水位、守恒逐组约束；2429211 p8将目标与模型并列 | 每组公式解释控制的实际行为、单位、适用条件；不贴代码截图 |
| Our Work | 2102199 p5、2419984 p4、2509557 p5分区清楚 | 总图保留输入、机理、运输/水耦合、验证、推荐五层；不堆20个算法名 |
| 定量摘要 | 2419984规定时间的搜索指标；2501687有行动量；2509557偏概念性 | 选3–4个已溯源的数值，说明情景、基准、量纲及最优性范围 |
| 参数透明度 | 2509557 p15列来源；2502617 p7区分来源与Estimate | 将题给、文献、情景、标定/推导量分组，不把250次/基地/年当题给事实 |
| 对照与验证 | 2503268 p19基准柱图；2429211 p16目标/实现曲线 | 基准、独立约束检查、复跑、敏感性分开；不能互相替代 |
| 敏感性 | 2509557 p18–19双参数热图；2116496 p21多目标分量 | 除目标变化外写清策略是否切换、约束是否失效；零可行方案也是结果 |
| 管理价值 | 2104673 p23预算表；2517929 p24建议+监测 | 推荐应有行动、触发条件、成本/工期代价与监测点 |
| 附页差异 | 2021常见预算申请，2022多为杂志文章，2024–25多为Memo | 随本题与老师要求决定一页Agency Letter；不混用这些交付形式 |
| 数学边界 | 2213970 p21承认启发式未必最优；2502617 p1对SLSQP作过强宣称 | 获奖不等于结论可照搬；本项目目录最优、上界、鲁棒证书须限定范围 |
| 不宜模仿 | 2207864立体饼图、2505199密集小图；2127300附件队号冲突 | 简化视觉编码；做最终元数据、页眉与跨章节数值一致性检查 |

## 逐篇分析

<a id="team-2102199"></a>

### 2021 B / 2102199 — Build an Army of Drones to Fight Wildfires

[PDF](2021/MCM_B/2102199.pdf) · [实际页面](_reading/2102199/detail-sheet.jpg) · [补充页面](_reading/2102199/supplement-sheet.jpg)

**证据范围**：目视物理页1, 5, 7, 11, 19, 21, 22；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 按部署、极端事件、地形扩展串联，摘要逐模型给出任务与输出；篇幅偏密。 |
| Our Work与章节逻辑 | 借鉴Q2故障输入→服务能力→预算影响的表达。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设紧随解释，p6符号表；忽略天气等条件必须随结论披露。 |
| Mathematical Model Formulation / Solution Method | 栅格多目标优化；Poisson极端事件；Tabu Search。p11决策变量、目标与约束分列；搜索算法是求解手段，不保证全局最优。 |
| Results and Interpretation | p12部署结果连到p22–23预算，形成空间配置→采购的决策链。 |
| Sensitivity Analysis | p19–20分别扰动事件频率与输入；局部扰动不能证明跨区域普适性。 |
| Strengths and Weaknesses | p21承认位置数据和前线人员简化；摘要关于Tabu Search全局效果的措辞不宜借用。 |
| Recommendation Letter / 其他决策者附页 | p22–23 Budget Request含区域理由和成本表。 |
| 图表、字体、配色、信息密度 | p5流程分区清楚；p7数据表与地图并置；地图标签偏小、摘要加粗较多。 |

**OR迁移取舍**：借鉴Q2故障输入→服务能力→预算影响的表达。 学习解释和论证，不移植该题模型或数值。

<a id="team-2104673"></a>

### 2021 B / 2104673 — ‘Rapid Bushfire Response’ UAV System

[PDF](2021/MCM_B/2104673.pdf) · [实际页面](_reading/2104673/detail-sheet.jpg) · [补充页面](_reading/2104673/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 18, 20, 23；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 先观测任务再未来火情再地形，结果汇总单列，读者易回到问题。 |
| Our Work与章节逻辑 | 借鉴Report结尾“建议+条件+采购/执行依据”。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4列出不发生无人机故障的假设；此条件与本项目Q2恰好不同。 |
| Mathematical Model Formulation / Solution Method | 区域离散优化；元胞自动机；地形通信约束。p18把覆盖收益、无人机数量及通信限制写成紧凑模型，并给出求解工具。 |
| Results and Interpretation | p18–19按问题汇总部署；p23逐设备数量与单价更接近可执行采购。 |
| Sensitivity Analysis | p16–17扰动探测能力和边界参数，区分各参数的作用。 |
| Strengths and Weaknesses | p20明确气象、火情数据和植被限制；不把情景模拟视作实际预测验证。 |
| Recommendation Letter / 其他决策者附页 | p22信件与p23预算表互补，正文不重复全部算法。 |
| 图表、字体、配色、信息密度 | p4示意图和流程图分开；p23有单位、数量、用途，但窄列换行较挤。 |

**OR迁移取舍**：借鉴Report结尾“建议+条件+采购/执行依据”。 学习解释和论证，不移植该题模型或数值。

<a id="team-2105363"></a>

### 2021 B / 2105363 — Rapid Bushfire Response for Emergency Response

[PDF](2021/MCM_B/2105363.pdf) · [实际页面](_reading/2105363/detail-sheet.jpg) · [补充页面](_reading/2105363/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 9, 21, 23；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 从风险分区推到装备数，再讨论极端事件及地形，摘要有明确数量输出。 |
| Our Work与章节逻辑 | 借鉴设备/电力/库存计量的正文解释，避免只贴JSON。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p3假设、p4符号和航程图；航程单位与变量关系就近解释。 |
| Mathematical Model Formulation / Solution Method | 风险分区；数量与成本优化；贪心混合；信号损失。p9目标与成本构成分层，p12伪代码声明输入/输出；算法与数学模型可追踪。 |
| Results and Interpretation | p13用权衡图呈现能力与成本，避免只报单一数量。 |
| Sensitivity Analysis | p21–22对安全因子权重和火频分地区分析；加权指标需说明主观性。 |
| Strengths and Weaknesses | p23承认模拟数据与AHP权重局限，可借鉴局限的具体对象。 |
| Recommendation Letter / 其他决策者附页 | p23–25 Annotated Budget Request有设备分解。 |
| 图表、字体、配色、信息密度 | p4三线式符号表和插图紧邻公式；p21并排场景图可比，色彩较多。 |

**OR迁移取舍**：借鉴设备/电力/库存计量的正文解释，避免只贴JSON。 学习解释和论证，不移植该题模型或数值。

<a id="team-2116496"></a>

### 2021 B / 2116496 — Drone System VS Wildfire

[PDF](2021/MCM_B/2116496.pdf) · [实际页面](_reading/2116496/detail-sheet.jpg) · [补充页面](_reading/2116496/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 6, 10, 21, 23, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 四步部署由前线人员到EOC、通信再SSA，输入输出关系明确。 |
| Our Work与章节逻辑 | 借鉴把成本与安全的取舍写成可解释推荐。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p3–4假设与符号；p6按四步骤说明数据如何进入决策。 |
| Mathematical Model Formulation / Solution Method | GMM；K-means；最小生成树；AHP/TOPSIS；灰色预测。p10图解Kruskal通信网络，模型原理和局部几何关系并列。 |
| Results and Interpretation | p14对两个月分别给出方案；p25转为数量、费用与总预算。 |
| Sensitivity Analysis | p21–22同时追踪安全、经济等分项及总指标，便于解释权衡拐点。 |
| Strengths and Weaknesses | p23指出未测因素和地形成本省略；泛化与稳定性仍需超出作者自述的证据。 |
| Recommendation Letter / 其他决策者附页 | p25一页Budget Request含简图、明细表和请求金额。 |
| 图表、字体、配色、信息密度 | Serif正文、细页眉、分项曲线；曲线颜色靠图例区分，灰度下应补线型。 |

**OR迁移取舍**：借鉴把成本与安全的取舍写成可解释推荐。 学习解释和论证，不移植该题模型或数值。

<a id="team-2127300"></a>

### 2021 B / 2127300 — Rapid Bushfire Response System

[PDF](2021/MCM_B/2127300.pdf) · [实际页面](_reading/2127300/detail-sheet.jpg) · [补充页面](_reading/2127300/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 17, 19, 21, 22, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。p24–25页眉队号2120188与主体2127300不同，附件身份待核。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 采购、未来极端火情、地形部署按子问展开；摘要给基础与追加预算。 |
| Our Work与章节逻辑 | 借鉴基础/故障追加成本分表；警惕模板页眉与身份残留。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4假设与参数，p21高度扰动；训练预测与部署假设应分开。 |
| Mathematical Model Formulation / Solution Method | 遗传算法；LSTM；无线传播损失；地形优化。p10以后搜索EOC与中继位置；p19地形附加约束解释方案变化。 |
| Results and Interpretation | p22–23结果表回收各题答案，正文信息可转入预算。 |
| Sensitivity Analysis | p21以飞行高度扰动检查通信范围；不能替代预测模型的样本外检验。 |
| Strengths and Weaknesses | p22承认仅用短期火情数据；p24–25页眉出现2120188，与主体队号冲突，附件完整性存疑。 |
| Recommendation Letter / 其他决策者附页 | p24预算信署名2127300但页眉不同；仅学习结构，不视附件身份已认证。 |
| 图表、字体、配色、信息密度 | p17/19空间分布与地形图分工清楚；p21长小数坐标过密。 |

**OR迁移取舍**：借鉴基础/故障追加成本分表；警惕模板页眉与身份残留。 学习解释和论证，不移植该题模型或数值。

<a id="team-2200084"></a>

### 2022 B / 2200084 — A Model for Better Use of Water Resources Based on Marginal Utility and Auction Theory

[PDF](2022/MCM_B/2200084.pdf) · [实际页面](_reading/2200084/detail-sheet.jpg) · [补充页面](_reading/2200084/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 9, 11, 18, 20, 23, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 先可行资源网络，再利益度量，再短缺分配；模型之间有明确依赖。 |
| Our Work与章节逻辑 | 借鉴建设期→入住期资源网络及停止/失效条件的写法。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设与符号；圆柱近似的影响在p20回收。 |
| Mathematical Model Formulation / Solution Method | 时变LP；资源网络；边际效用；独立私人价值拍卖。p9伪代码列状态、逐期求解与终止条件；不是只展示库调用。 |
| Results and Interpretation | p10–11时间序列联系服务持续时间和分配方案。 |
| Sensitivity Analysis | p18–19需求、能源替代与节约措施；阶梯输出说明离散决策变化。 |
| Strengths and Weaknesses | p20明确几何近似和缺少实地测试；不能把经济理论本身当数值正确性。 |
| Recommendation Letter / 其他决策者附页 | p23–24面向大众的文章，而非Recommendation Letter。 |
| 图表、字体、配色、信息密度 | p4流程图模块依赖清楚；p11嵌套环图标签过密，不建议复刻。 |

**OR迁移取舍**：借鉴建设期→入住期资源网络及停止/失效条件的写法。 学习解释和论证，不移植该题模型或数值。

<a id="team-2202748"></a>

### 2022 B / 2202748 — Salvation in an Age of Water Scarcity

[PDF](2022/MCM_B/2202748.pdf) · [实际页面](_reading/2202748/detail-sheet.jpg) · [补充页面](_reading/2202748/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 6, 8, 22, 23, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 双库运输→多利益目标→边界地区→需求变化，顺着问题增加约束。 |
| Our Work与章节逻辑 | 借鉴水量守恒、处理能力与供应时间的分层解释。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5–6假设、符号及来源表；来源表不等于所有系数已可靠标定。 |
| Mathematical Model Formulation / Solution Method | 运输模型；多目标规划；维持时间迭代；墨西哥分配。p8解释水电转换与损失；p12迭代算法说明何时停止。 |
| Results and Interpretation | p13后计算取水与持续时间，p20多目标结果支持分配。 |
| Sensitivity Analysis | p22–23分别改变需求、效率、节约幅度；适合区分情景与敏感性。 |
| Strengths and Weaknesses | p24明确部分参数未知及发电来源简化。 |
| Recommendation Letter / 其他决策者附页 | p25杂志文章把技术结果转为公众建议。 |
| 图表、字体、配色、信息密度 | p6来源三线表有用；p22并排分组柱图文字偏小、类别多。 |

**OR迁移取舍**：借鉴水量守恒、处理能力与供应时间的分层解释。 学习解释和论证，不移植该题模型或数值。

<a id="team-2207864"></a>

### 2022 B / 2207864 — Water and Hydroelectric Power Sharing

[PDF](2022/MCM_B/2207864.pdf) · [实际页面](_reading/2207864/detail-sheet.jpg) · [补充页面](_reading/2207864/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 5, 10, 21, 23, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 按水位阶段形成规则，强调在资源短缺时如何变更配置。 |
| Our Work与章节逻辑 | 借鉴预置、在建、入住阶段的阈值规则，不迁移水库模型。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4假定短期忽略蒸发降雨；与后续长期外推要区分。 |
| Mathematical Model Formulation / Solution Method | 等效库形；多目标调度；阶段划分；EWM-TOPSIS；0–1规划。p10从流量、日量到输水时间的公式衔接；单位转换需逐项核对。 |
| Results and Interpretation | p16–20阶段性配置比只报最优目标更能指导管理。 |
| Sensitivity Analysis | p21–22讨论技术与需求变化及灵敏度；图表应保留扰动的明确基准。 |
| Strengths and Weaknesses | p23承认时效数据及简化影响；不能照搬其参数或单位表述。 |
| Recommendation Letter / 其他决策者附页 | p25面向公众的方案页；不是正式推荐信。 |
| 图表、字体、配色、信息密度 | p5蓝色数据表易导航；3D饼图和立体金字塔造成面积/体积误读，应避免。 |

**OR迁移取舍**：借鉴预置、在建、入住阶段的阈值规则，不迁移水库模型。 学习解释和论证，不移植该题模型或数值。

<a id="team-2211922"></a>

### 2022 B / 2211922 — Reservoir Management: The Art of Proper Allocation

[PDF](2022/MCM_B/2211922.pdf) · [实际页面](_reading/2211922/detail-sheet.jpg) · [补充页面](_reading/2211922/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 9, 17, 19, 21, 23；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。封面年份2021与官方2022 B身份不一致。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 按数据→收支→模型→解→短缺扩展组织，逻辑链较完整。 |
| Our Work与章节逻辑 | 借鉴主文保留关键推导、长证明进入附录的分层。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4–5假设与符号；p1年份印为2021，官方身份是2022 B，保留此副本差异。 |
| Mathematical Model Formulation / Solution Method | 双库差分系统；多目标GA；PCA优先分配。p9网络与差分方程同页；完整解析推导放p22–23附录。 |
| Results and Interpretation | p17分配结果回连附表，正文解释用途与地区差异。 |
| Sensitivity Analysis | p17–18检验需求、节约、新能源；需要清楚区分政策改变和参数误差。 |
| Strengths and Weaknesses | p19承认需按情势重跑；不能把模型周期当实际水文规律。 |
| Recommendation Letter / 其他决策者附页 | p20–21双栏杂志版，面向读者解释意外发现与建议。 |
| 图表、字体、配色、信息密度 | 流程图+方程配对好；发光环图不利精确比较；双栏文章需控制照片占比。 |

**OR迁移取舍**：借鉴主文保留关键推导、长证明进入附录的分层。 学习解释和论证，不移植该题模型或数值。

<a id="team-2213970"></a>

### 2022 B / 2213970 — Decision System for Optimizing Water Allocation

[PDF](2022/MCM_B/2213970.pdf) · [实际页面](_reading/2213970/detail-sheet.jpg) · [补充页面](_reading/2213970/supplement-sheet.jpg)

**证据范围**：目视物理页1, 6, 15, 19, 21, 22, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 先物理分配，再竞争利益，再短缺规则和干预变化，摘要按题回答。 |
| Our Work与章节逻辑 | 借鉴本项目有限目录最优、闭式界与LP复核范围的准确措辞。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5–6假设、符号、数据；符号表含单位，便于量纲检查。 |
| Mathematical Model Formulation / Solution Method | 非线性规划/模拟退火；博弈/Newton；短缺指标迭代。p15收益函数接均衡一阶条件与Newton求根；求根不自动证明均衡存在/最优。 |
| Results and Interpretation | p15对照基本需求与均衡分配，有比较基准。 |
| Sensitivity Analysis | p19–20明确均衡可能落在需求范围之外，检查可用性比泛称稳定更有价值。 |
| Strengths and Weaknesses | p21直言启发式结果未必最优，是可借鉴的证据边界。 |
| Recommendation Letter / 其他决策者附页 | p22有面向普通读者的研究介绍文章；未见独立Recommendation Letter标题，不能把代码附录误判为整份附件。 |
| 图表、字体、配色、信息密度 | p6分区流程与单位表较好；多面板月曲线偏小。 |

**OR迁移取舍**：借鉴本项目有限目录最优、闭式界与LP复核范围的准确措辞。 学习解释和论证，不移植该题模型或数值。

<a id="team-2228168"></a>

### 2022 B / 2228168 — A Two-Stage Water Resource Optimal Operation Model Based on Genetic Algorithm

[PDF](2022/MCM_B/2228168.pdf) · [实际页面](_reading/2228168/detail-sheet.jpg) · [补充页面](_reading/2228168/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 6, 8, 20, 22, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 先最小输送成本，再经济分配，再短缺调度，按任务递进。 |
| Our Work与章节逻辑 | 借鉴本项目变量→约束→证书→结果的技术表达。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4–5假设解释起点、目标点与单位运输成本；空间近似影响成本。 |
| Mathematical Model Formulation / Solution Method | LP运输；两阶段规划；精英GA；差分进化。p6–12将需求、水位、守恒、出流逐组列约束；读者可逐组核验。 |
| Results and Interpretation | p20收敛图与变量/单位/结果表同页；曲线收敛不是全局最优证明。 |
| Sensitivity Analysis | p20–21针对库容和需求下降给情景，不能称统计置信区间。 |
| Strengths and Weaknesses | p22–23说明固定时段与地理简化的局限。 |
| Recommendation Letter / 其他决策者附页 | p24面向杂志的文章，重述主要情景结果。 |
| 图表、字体、配色、信息密度 | p8几何示意清楚；三线结果表优于贴代码；正文小数分组应统一。 |

**OR迁移取舍**：借鉴本项目变量→约束→证书→结果的技术表达。 学习解释和论证，不移植该题模型或数值。

<a id="team-2407038"></a>

### 2024 B / 2407038 — Unlocking the Abyss: A Dynamical Model for Deep-Sea Adventure Safety and Rescue Strategies

[PDF](2024/MCM_B/2407038_reformship.pdf) · [实际页面](_reading/2407038/detail-sheet.jpg) · [补充页面](_reading/2407038/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 13, 15, 22, 23, 24, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。原GitHub副本文字重叠；另用reformship副本。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 定位→备装→搜索，前一模型输出服务下一决策；摘要基本完整。 |
| Our Work与章节逻辑 | 借鉴“预测/机理计算→资源配置→服务效果”的单条证据链。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设与符号，p6数据处理；传感信息、环境参数和可控装备需区分。 |
| Mathematical Model Formulation / Solution Method | ARIMA/岭回归；动力学；GA装备权衡；Bayes栅格搜索。p13逐一解释成本、维护、可用性、使用与准备时间；p15给权衡解。 |
| Results and Interpretation | p15候选表和Pareto图共同支持设备选择，不能把图上离散点连成可行连续面。 |
| Sensitivity Analysis | p22改变搜索时间间隔，比较累计概率和偏差。 |
| Strengths and Weaknesses | p23模型评价；转海域情景属于可迁移性演示，非外部实测验证。 |
| Recommendation Letter / 其他决策者附页 | p23–24政府Memo列装备、搜索与安全措施；不能把它自动当课程所需的一页推荐信。 |
| 图表、字体、配色、信息密度 | 原镜像文字重叠，改用reformship可读入口；p4流程清楚但细节密。 |

**OR迁移取舍**：借鉴“预测/机理计算→资源配置→服务效果”的单条证据链。 学习解释和论证，不移植该题模型或数值。

<a id="team-2411570"></a>

### 2024 B / 2411570 — From Lost to Found: Roam in the Ionian Sea

[PDF](2024/MCM_B/2411570_reformship.pdf) · [实际页面](_reading/2411570/detail-sheet.jpg) · [补充页面](_reading/2411570/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 9, 20, 21, 23；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。原GitHub下载副本解析为0页；另用reformship副本。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 环境动力→装备评分→搜索→推广，模型角色明确；摘要定量结果不足。 |
| Our Work与章节逻辑 | 借鉴物理单位表与变量初值说明，避免摘要只有方法名。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p6符号和假设；p9用表说明尺寸、速度和初始条件。 |
| Mathematical Model Formulation / Solution Method | 微分动力学；EWM-TOPSIS；Monte Carlo；改进圆形搜索。p9参数表与坐标图先于动力方程，p10–11解释扰动与阻力。 |
| Results and Interpretation | 搜索概率随时间变化帮助回答动作效果，不只是轨迹图。 |
| Sensitivity Analysis | p20–21分别改变流速和阻力；三维柱阵过密，难读具体效应。 |
| Strengths and Weaknesses | p21指出参数依赖实测；不能以漂亮曲面代替误差数值。 |
| Recommendation Letter / 其他决策者附页 | p23–24Memo按定位、装备、搜救及推广组织。 |
| 图表、字体、配色、信息密度 | 原GitHub副本解析为0页；reformship副本可读。冷蓝配色统一，坐标示意有效。 |

**OR迁移取舍**：借鉴物理单位表与变量初值说明，避免摘要只有方法名。 学习解释和论证，不移植该题模型或数值。

<a id="team-2419984"></a>

### 2024 B / 2419984 — Time is Life: Precise Localization and Faster Search

[PDF](2024/MCM_B/2419984.pdf) · [实际页面](_reading/2419984/detail-sheet.jpg) · [补充页面](_reading/2419984/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 6, 18, 22, 23, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 按定位、设备、搜索、扩展串联，摘要给定时域的搜索成功指标。 |
| Our Work与章节逻辑 | 借鉴Q2故障→结果变化→为何应采取动作，而非只列故障因子。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4假设接流程，p5符号，p6设备参数；初态/故障不确定性单列。 |
| Mathematical Model Formulation / Solution Method | RK4；动力学；熵权成本效益；Monte Carlo；ACO/Bayes。p18把后验更新、累计探测概率与时间权重连接，再给搜索策略。 |
| Results and Interpretation | p19–20搜索曲线对应时限和启动时间，强调启动时机的管理意义。 |
| Sensitivity Analysis | p22扰动阻力系数并给水平/深度偏差范围。 |
| Strengths and Weaknesses | p23明确估计阻力和离散时间误差；本轮未复现概率与路径。 |
| Recommendation Letter / 其他决策者附页 | p24–25Memo含搜索示意与设备建议。 |
| 图表、字体、配色、信息密度 | p4框架有明确模型边界；p22局部放大清楚，但3D图需更大轴字号。 |

**OR迁移取舍**：借鉴Q2故障→结果变化→为何应采取动作，而非只列故障因子。 学习解释和论证，不移植该题模型或数值。

<a id="team-2425792"></a>

### 2024 B / 2425792 — Save the Submersible: An Combined Method of Computational Fluid Dynamics and Kalman Filter

[PDF](2024/MCM_B/2425792.pdf) · [实际页面](_reading/2425792/detail-sheet.jpg) · [补充页面](_reading/2425792/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 9, 21, 24, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 以定位、准备、搜索、扩展的动作组织摘要，可快速理解用途。 |
| Our Work与章节逻辑 | 借鉴明确数学条件与误差量定义；不将本项目确定性证书写成统计置信。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5–7参数与假设；滤波的状态、观测与噪声条件应显式交代。 |
| Mathematical Model Formulation / Solution Method | 简化6DOF；Kalman Filter；PCA；Voronoi。p8–9动力模型和预测/更新公式相连，图解释不确定性更新。 |
| Results and Interpretation | 以空间范围和搜索方案表达结果；所谓95%空间需解释概率对象与噪声假设。 |
| Sensitivity Analysis | p21同时给扰动相似度与RMSE，优于只说“鲁棒”；真实轨迹来源尚未本轮核验。 |
| Strengths and Weaknesses | p22评价；p25的广泛可移植性仍应限定条件。 |
| Recommendation Letter / 其他决策者附页 | p24–25Memo按定位、减小不确定性、搜索和装备解释。 |
| 图表、字体、配色、信息密度 | Serif正文、公式对齐、3D受力示意有解释作用；三维轨迹不适合所有指标。 |

**OR迁移取舍**：借鉴明确数学条件与误差量定义；不将本项目确定性证书写成统计置信。 学习解释和论证，不移植该题模型或数值。

<a id="team-2417004"></a>

### 2024 D / 2417004 — Regulating the Water of Tomorrow: A Multi-Layer Optimization Model for the Great Lakes

[PDF](2024/ICM_D/2417004.pdf) · [实际页面](_reading/2417004/detail-sheet.jpg) · [补充页面](_reading/2417004/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 5, 16, 19, 23；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 基本网络→复杂流量→利益目标→2017检查，渐进建模主线清楚。 |
| Our Work与章节逻辑 | 借鉴基础模型→已有扩展的叙述，不为版式而新增复杂模型。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4假设/符号；p5实景地图转抽象网络，有助理解系统边界。 |
| Mathematical Model Formulation / Solution Method | 网络水流；进阶气象模型；NSGA-II；多元回归。p16利益函数与目标就近解释；应区分历史水位范围与安全硬约束。 |
| Results and Interpretation | p19把2017月水位与区间叠加；落入区间本身不足以证明策略更优。 |
| Sensitivity Analysis | p19–20分别分析降水与雪等影响；区分季节带与不确定性区间。 |
| Strengths and Weaknesses | p21–22评价；摘要“所有利益相关者受益”需要分项对照，不宜移植强结论。 |
| Recommendation Letter / 其他决策者附页 | p23给IJC一页Memo，说明继承与改善的管理内容。 |
| 图表、字体、配色、信息密度 | 绿色网络、分组流程和季节背景带易导航；颜色区间必须有语义。 |

**OR迁移取舍**：借鉴基础模型→已有扩展的叙述，不为版式而新增复杂模型。 学习解释和论证，不移植该题模型或数值。

<a id="team-2417831"></a>

### 2024 D / 2417831 — Harmony of the Great Lakes: A Water Level Balance Approach

[PDF](2024/ICM_D/2417831.pdf) · [实际页面](_reading/2417831/detail-sheet.jpg) · [补充页面](_reading/2417831/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 9, 10, 23, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 先目标水位，再控制算法，再极端天气，明确目标与执行不同。 |
| Our Work与章节逻辑 | 借鉴“评价标准→可行执行策略→情景后果”的章节衔接。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p3–4假设与单位表，p10地理数据；单位表需对每项一致。 |
| Mathematical Model Formulation / Solution Method | GA/AHP利益目标；湖链水动力；预测反馈控制。p9湖链示意、物理方程和控制设计衔接；不能只画算法名称框。 |
| Results and Interpretation | p16以后比较模拟与基准水位，并讨论上下游影响。 |
| Sensitivity Analysis | 极端降水/冰塞与控制出流变化分组；p23指出利益权重需更专业依据。 |
| Strengths and Weaknesses | p23承认利益群体及盆地范围不完整；不能据AHP权重称客观最优。 |
| Recommendation Letter / 其他决策者附页 | p24IJC Memo传达目标和控制方案；量化比较可更集中。 |
| 图表、字体、配色、信息密度 | p4多区框架清楚但文字密；p10表格、地图与守恒逻辑就近。 |

**OR迁移取舍**：借鉴“评价标准→可行执行策略→情景后果”的章节衔接。 学习解释和论证，不移植该题模型或数值。

<a id="team-2419588"></a>

### 2024 D / 2419588 — Optimizing Great Lakes Water Management: An Adaptive Hydrological Network Approach

[PDF](2024/ICM_D/2419588.pdf) · [实际页面](_reading/2419588/detail-sheet.jpg) · [补充页面](_reading/2419588/supplement-sheet.jpg)

**证据范围**：目视物理页1, 3, 5, 6, 22, 25, 27；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。封面题号C与官方2024 D身份不一致。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 网络→利益度量→控制→极端情景，摘要主动写出局限，结果定量不足。 |
| Our Work与章节逻辑 | 借鉴“具体省略→受影响决策→需要怎样验证”的局限写法。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4–5假设符号；封面题号为C而官方队号对应D，副本与原提交完全一致性未确认。 |
| Mathematical Model Formulation / Solution Method | 水文网络；利益满意度ESS；MPC。p6先说明面积近似再给水量平衡；利益函数需经验依据。 |
| Results and Interpretation | 强调2017及高水位响应；多数可信度表述不能代替误差/基准数字。 |
| Sensitivity Analysis | p19–22按降水、积雪、冰塞讨论失败响应，可借鉴负面表现披露。 |
| Strengths and Weaknesses | p22明确时滞、支流/地下水省略和利益函数待验证。 |
| Recommendation Letter / 其他决策者附页 | p25为宣传式方案页，不当作已确认的正式Recommendation Letter。 |
| 图表、字体、配色、信息密度 | p5蓝色符号表、p25海报层级清楚；宣传词与背景装饰不宜进入技术结论。 |

**OR迁移取舍**：借鉴“具体省略→受影响决策→需要怎样验证”的局限写法。 学习解释和论证，不移植该题模型或数值。

<a id="team-2429211"></a>

### 2024 D / 2429211 — Dynamic Dams Model: A Multigranular, Human-Centered Approach For Modeling Water In The Great Lakes

[PDF](2024/ICM_D/2429211.pdf) · [实际页面](_reading/2429211/detail-sheet.jpg) · [补充页面](_reading/2429211/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 10, 16, 18, 19, 20, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 月尺度目标与日尺度执行分开，再把管理洞见集中写出；适合OR读者。 |
| Our Work与章节逻辑 | 首选：借鉴本项目运输与入住两阶段、有限候选优化的清晰表达。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设；p21–22附录区分集合、参数、变量，减轻正文负担。 |
| Mathematical Model Formulation / Solution Method | 动态流网络；宏/微两层LP；时滞相关；线性回归。p8在目标下逐组列约束，p12接微观调度；绝对值目标的线性化应另解释。 |
| Results and Interpretation | p14–16基准/极端气候曲线配文字，强调不可避免洪水的可管理性。 |
| Sensitivity Analysis | p16–17改流量衰减并讨论控制能力；不是宣称能消除所有风险。 |
| Strengths and Weaknesses | p18–19说明权重、数据细度和未来检验；机制模型仍依赖参数。 |
| Recommendation Letter / 其他决策者附页 | p20IJC Memo把模型转为建议，正文不复述全部推导。 |
| 图表、字体、配色、信息密度 | p10相关图旁紧接时滞矩阵；实线/虚线区分目标/实现，灰度也可读。 |

**OR迁移取舍**：首选：借鉴本项目运输与入住两阶段、有限候选优化的清晰表达。 学习解释和论证，不移植该题模型或数值。

<a id="team-2501687"></a>

### 2025 B / 2501687 — Economy, Ecology, and Social Welfare: A Win-Win Approach for Sustainable Tourism in Juneau

[PDF](2025/MCM_B/2501687.pdf) · [实际页面](_reading/2501687/detail-sheet.jpg) · [补充页面](_reading/2501687/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 13, 17, 22, 23, 24, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 从经济/环境/社会影响转为可控政策，再比较另一目的地。 |
| Our Work与章节逻辑 | 借鉴推荐方案说明“何时、多少、用于什么”，不引入CVM替代现有成本模型。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设与符号；货币化系数属于估计/价值判断，应与观测数据区分。 |
| Mathematical Model Formulation / Solution Method | CVM货币化；多目标非线性规划；PSO；情景比较。p8写目标和最低环境/社会要求，p13展示参数选择与诊断图。 |
| Results and Interpretation | 摘要给游客限制与投资组合，p25Memo给可执行政策；正文与信件需同口径。 |
| Sensitivity Analysis | p17–18曲线显示政策变量效应，不能把局部稳定当现实政策有效。 |
| Strengths and Weaknesses | p22–23评价；需审视估值与地区迁移条件，本轮未核验其外部数据。 |
| Recommendation Letter / 其他决策者附页 | p25冰川背景Memo；内容有行动与量化值，背景影响文字对比。 |
| 图表、字体、配色、信息密度 | 摘要重点加粗克制于关键结果；流程图分组好；避免整页照片作正文底图。 |

**OR迁移取舍**：借鉴推荐方案说明“何时、多少、用于什么”，不引入CVM替代现有成本模型。 学习解释和论证，不移植该题模型或数值。

<a id="team-2502617"></a>

### 2025 B / 2502617 — Overload Alarm: Pareto Optimization of the Economic-Social-Environmental Triangle

[PDF](2025/MCM_B/2502617.pdf) · [实际页面](_reading/2502617/detail-sheet.jpg) · [补充页面](_reading/2502617/supplement-sheet.jpg)

**证据范围**：目视物理页1, 5, 7, 14, 20, 21, 25, 26；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。摘要文本层为空，队号已通过渲染p1目视确认。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 三种利益各自建式后整合，先解释可比性，再给政策。 |
| Our Work与章节逻辑 | 借鉴目标/权重/约束同页呈现；本项目保留有限目录证据范围。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5假设与p7参数来源/估计表；隐藏成本货币化依赖权重选择。 |
| Mathematical Model Formulation / Solution Method | 成本效益；福利/生态承载；加权非线性优化；SLSQP。p14列多目标、加权目标及可行约束，便于理解决策空间。 |
| Results and Interpretation | 摘要给客流与收益；把SLSQP输出称全球Pareto最优缺少充分证明，不能照学。 |
| Sensitivity Analysis | p20–21单变量曲线与总利益变化，需区分相关图与因果效应。 |
| Strengths and Weaknesses | p21明确时间滞后和空间竞争省略。 |
| Recommendation Letter / 其他决策者附页 | p25Memo；p26AI记录为独立附件，不能套用其AI规则。 |
| 图表、字体、配色、信息密度 | p1图像型文字使文本提取为空；视觉确认队号。参数三线表清楚，环形图难精确比较。 |

**OR迁移取舍**：借鉴目标/权重/约束同页呈现；本项目保留有限目录证据范围。 学习解释和论证，不移植该题模型或数值。

<a id="team-2503268"></a>

### 2025 B / 2503268 — Rebalancing Nature’s Scale: A Model to Tame Overtourism

[PDF](2025/MCM_B/2503268.pdf) · [实际页面](_reading/2503268/detail-sheet.jpg) · [补充页面](_reading/2503268/supplement-sheet.jpg)

**证据范围**：目视物理页1, 2, 3, 4, 5, 11, 16, 19, 20, 24, 26；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 动力系统→有限干预组合→评分反馈→基准比较，模型互相有接口。 |
| Our Work与章节逻辑 | 借鉴有限策略集、基准对照与参数估计诚实披露。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5–7假设、符号与数据选择；p16承认部分参数经验估计。 |
| Mathematical Model Formulation / Solution Method | 旅游ODE；Lotka–Volterra/Logistic/SIS启发；AHP；Morris。p9–16动力与评价模型分开；不要把评价分数当物理量。 |
| Results and Interpretation | p19同图比较基准与策略，能够指出收益来自哪项比较。 |
| Sensitivity Analysis | p19–21同时用Morris与局部灵敏度；其预测任务不意味着本项目也需同算法。 |
| Strengths and Weaknesses | p24 Strengths and Weaknesses须从渲染阅读；推广到Big Sur不自动证明普适。 |
| Recommendation Letter / 其他决策者附页 | p2装饰性Memo置于目录前，正文可检索性较弱。 |
| 图表、字体、配色、信息密度 | p19分组柱图清楚；羊皮纸式Memo和极小多面板不宜复制到课程技术报告。 |

**OR迁移取舍**：借鉴有限策略集、基准对照与参数估计诚实披露。 学习解释和论证，不移植该题模型或数值。

<a id="team-2504448"></a>

### 2025 B / 2504448 — Sustainable Tourism Management in Juneau

[PDF](2025/MCM_B/2504448.pdf) · [实际页面](_reading/2504448/detail-sheet.jpg) · [补充页面](_reading/2504448/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 6, 12, 13, 17, 23, 24, 25；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 一个游客需求输入三种效应，再回到预算政策，模型角色易理解。 |
| Our Work与章节逻辑 | 借鉴明确递推与预算反馈，但本项目无需新建动态规划。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4–6假设、数据与量纲；仅五年数据的影响在p23明确。 |
| Mathematical Model Formulation / Solution Method | 需求递推；经济/环境/满意度；动态规划；熵权。p12环境恢复与满意度式接决策流程；动态规划须写状态/动作/递推。 |
| Results and Interpretation | 报告五年政策变化、税率与分配；应区分模型模拟与真实未来预测。 |
| Sensitivity Analysis | p17–18分别扰动环境和满意度输入，分项曲线帮助解释资源转移。 |
| Strengths and Weaknesses | p23列数据、固定恢复率、利益群体和计算开销限制。 |
| Recommendation Letter / 其他决策者附页 | p24标准Memo含动作建议，适合学习面向决策者的简洁结构。 |
| 图表、字体、配色、信息密度 | p4有方向的模型框架、p6紧凑数据表；多曲线图可改直接标注。 |

**OR迁移取舍**：借鉴明确递推与预算反馈，但本项目无需新建动态规划。 学习解释和论证，不移植该题模型或数值。

<a id="team-2505199"></a>

### 2025 B / 2505199 — Breaking through the Tourism Dilemmas in Juneau: The Road to Sustainable Development Driven by a Multi-objective Model

[PDF](2025/MCM_B/2505199.pdf) · [实际页面](_reading/2505199/detail-sheet.jpg) · [补充页面](_reading/2505199/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 20, 21, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 按决策变量、三个目标、约束、解集与推广组织，摘要给政策组合。 |
| Our Work与章节逻辑 | 作为反例提醒本项目信件、摘要、预算表必须同源。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p4–6假设符号，p8解释可控投资变量和指标关系。 |
| Mathematical Model Formulation / Solution Method | 多目标非线性优化；NSGA-II；拟合；多参数情景。p8以后逐项构建目标函数，p18–19说明算法与解集。 |
| Results and Interpretation | p24Memo与p1摘要存在税率/收费及分配口径差异，副本内一致性须核对，不能当范式照抄。 |
| Sensitivity Analysis | p20单参数与多参数矩阵并列；小图过密且难读精确差异。 |
| Strengths and Weaknesses | p21坦承静态模型与区域竞争局限；建议深度学习不自动构成必要改进。 |
| Recommendation Letter / 其他决策者附页 | p24Memo层级清楚，需先检查数字与摘要一致。 |
| 图表、字体、配色、信息密度 | p4分组框架有用；3D饼图、3D前沿和密集矩阵应换更可读的二维图。 |

**OR迁移取舍**：作为反例提醒本项目信件、摘要、预算表必须同源。 学习解释和论证，不移植该题模型或数值。

<a id="team-2509557"></a>

### 2025 B / 2509557 — The Triangular Balance of Environment, Economy, and Society: A System Dynamics-Based Model for Sustainable Tourism Management

[PDF](2025/MCM_B/2509557.pdf) · [实际页面](_reading/2509557/detail-sheet.jpg) · [补充页面](_reading/2509557/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 5, 8, 15, 17, 18, 19, 23, 25, 26；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 因果反馈→方程→参数→仿真→政策阶段，摘要逻辑清楚但缺核心数字。 |
| Our Work与章节逻辑 | 借鉴参数溯源表与参数组合的管理解释，不导入旅游ODE。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p8概览与假设，p11符号，p15参数表写来源，区分标定与假设。 |
| Mathematical Model Formulation / Solution Method | 系统动力学；非线性反馈；L-BFGS-B；情景与迁移。p12–14四状态与税收中介衔接，变量作用域较清楚。 |
| Results and Interpretation | p17四联图解释政策后的动态；拟合与政策效果不能混为同一证据。 |
| Sensitivity Analysis | p18–20交互热图及阶段策略，可学习阈值与组合解释。 |
| Strengths and Weaknesses | p23指出固定承载力、数据依赖和输入范围限制。 |
| Recommendation Letter / 其他决策者附页 | p25Memo是图像页，需渲染；不能因文本为空判断未交。 |
| 图表、字体、配色、信息密度 | p15来源表好；p17统一四联图便于串读；浅色线条需增强对比。 |

**OR迁移取舍**：借鉴参数溯源表与参数组合的管理解释，不导入旅游ODE。 学习解释和论证，不移植该题模型或数值。

<a id="team-2517929"></a>

### 2025 B / 2517929 — From TBMP to TSMP: Juneau’s Tourism Never Ends

[PDF](2025/MCM_B/2517929.pdf) · [实际页面](_reading/2517929/detail-sheet.jpg) · [补充页面](_reading/2517929/supplement-sheet.jpg)

**证据范围**：目视物理页1, 4, 8, 16, 23, 24；全篇文本可检索（部分页文本缺层），章节定向研读；计算复现NOT_RUN。第三方公开副本；未与COMAP会员版逐字比对。

| 读者功能 | 本次观察与评价 |
| --- | --- |
| Abstract / Summary Sheet；Introduction；Problem Analysis | 从目标优化到预算反馈再地区推广，额外模型由边界解现象引出。 |
| Our Work与章节逻辑 | 借鉴边界解→管理瓶颈的讨论，避免本项目无依据增添算法。 与下述方法及视觉证据结合阅读；不机械复制目录。 |
| Assumptions and Notations | p5–7假设符号来源；年数据忽略季节在p23承认。 |
| Mathematical Model Formulation / Solution Method | 多目标NSGA-II；回归/AHP；支出反馈；局部扰动。p8先目标与研究逻辑，p16给算法流程和有限解集。 |
| Results and Interpretation | 摘要与Memo解释限制客流、税费及基础设施投资，体现从解到行动。 |
| Sensitivity Analysis | 局部扰动热图用于关键因素排序；相关系数不证明政策因果。 |
| Strengths and Weaknesses | p23承认季节性与景点交互缺失；一处迁移案例不能称普适。 |
| Recommendation Letter / 其他决策者附页 | p24Memo列建议和后续监测，指标能用于实施反馈。 |
| 图表、字体、配色、信息密度 | p16算法图可读但基础算法说明占幅大；三维Pareto图缩小后难定位。 |

**OR迁移取舍**：借鉴边界解→管理瓶颈的讨论，避免本项目无依据增添算法。 学习解释和论证，不移植该题模型或数值。

## 本次识别的副本和论证风险

- 2411570初次GitHub副本被PyMuPDF识别为0页；2407038初次副本文字叠在一起。原件保留，可读入口换为用户指定reformship来源；两者哈希不同，不称“同一文件修复完成”。
- 2211922封面年份错误、2419588封面题号C、2127300附件页眉2120188均实际可见。官方奖项身份可以核实，但这些副本与官方原提交全文一致性不能据此认证。
- 2502617摘要的SLSQP全局性表述超出单靠算法名称可证明的范围。2102199摘要对Tabu Search的全局性类似。本轮指出的是表述/证据缺口，没有审计其原代码。
- 2505199 p1、p24在税费和收入分配口径上出现可见差异；只有回到同一批真实输出才能解决，不能以措辞润色掩盖。
- 跨地区再设参数、局部敏感性、收敛曲线、观测值落在范围内，分别提供不同证据，均不自动证明“普适、全局最优、预测准确”。

后续引用这些文章的方法或研究结论前，需补读原方法来源并核对适用条件；本库优先服务写作与制图训练。
