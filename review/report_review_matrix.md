# Report Review Matrix

2026-11-27；对象：根目录英文DOCX，SHA-256 `836aa1b8b31758a225185178c6b7ae4d117c216e63819215e99d6b80c9af91f7`。下表为只读审核和可执行改稿建议，未修改正文。负责人不预分配。CSV含完整九字段。段落号为零基 python-docx 索引，不能当渲染页码。

| Section | Priority | Problem / Evidence | Revision | Writer / Status |
| --- | --- | --- | --- | --- |
| Title | P0 | 封面是农业作物配置，正文是月球基地；report.1docx.docx 段1–3、50–55 | 重写题名并核对课程/日期/作者字段；先由两人确认报告身份；关联：原题Q1–Q5 | 待两人确认 / OPEN |
| Abstract | P1 | 未见独立摘要，关键问题/方法/结果未集中；段0–50 | 若教师要求，补目标—闭式上界/枚举—主要权衡—适用边界；不得称全局最优；关联：results/论文组结果表.csv | 待两人确认 / OPEN |
| Introduction | P2 | 任务存在，但研究问题和商业决策贡献可更清楚；段49–50 | 保留背景；补成本、工期、水安全与环境的冲突和决策者需求；关联：00_先读.md | 待两人确认 / OPEN |
| Problem Restatement | P1 | 2.x问题为普通段落，缺统一标题层级；段51–55 | 按Q1–Q5保留重述；明确信件是否属于课程交付；关联：COMAP 原题p2 | 待两人确认 / OPEN |
| Assumptions | P1 | 179000吨/年是单港还是系统总量待核；250发/年为情景；表1、construction_v9.py | 保留假设分类；说明外部仓储接收服务就绪、硬件增量、未来参数身份；重大变化先批准；关联：MCM_B_v9/proofs/ | 待两人确认 / OPEN |
| Notations | P2 | 表2含中文工作注；符号/公式编号混用；段64–65、85、102–117 | 统一变量、单位、域、下标；4Q/5Q/6Q与命名常数一一对应；关联：construction_v9.py service_parameters/_route_plan | 待两人确认 / OPEN |
| Mathematical Modeling | P1 | 硬件文字曾出现内含与增量矛盾，新版已统一增量；water_v9.py _aggregate、joint_v9.py hardware_ledger | 保留火箭质量链/服务曲线/库存；写100Mt仅通用建设物料，供水硬件另运另计；核对所有公式；关联：HARDWARE_ACCOUNTING | 待两人确认 / OPEN |
| Solution Methodology | P1 | 新版LP仅核验；主流程是闭式充分上界与有限目录；share_lp_check_v9.py、run_v9.py | 明确枚举流程、参数配置、可行证书；LP列验证附录，ODE列数值校验，不能称主流程MILP/单纯形；关联：新版20个PY | 待两人确认 / OPEN |
| Q1 Results | P2 | 数值未过时，图与类别最优份额口径不同；表4/5，Q1图固定30% E | 保留320.12/893.76/235.77年等；说明固定份额图和类别重选表区别；关联：论文组结果表、Q1图 | 待两人确认 / OPEN |
| Q2 Results | P2 | 固定份额与重新选择需分开，单因素分析未充分解释；段129–137，supplemental/q2_fault_attribution.csv | 保留故障上界；补固定/重选对照和瓶颈转移，不能写平均延误或概率；关联：16行故障表 | 待两人确认 / OPEN |
| Q3 Results | P2 | 毛用水、净消耗、初始库存容易混淆；段145–158，水结果表 | 保留1154.4t/day、421356t/year、21654.4t初始水；补包装比例103.618/125为团队假设；解释模块/舱/供电代价；关联：water_v9.py WaterInputs.packed_water_fraction | 待两人确认 / OPEN |
| Q4 Results | P2 | 环境仅代理，新增电网对照尚未充分进入正文；段167–173，low/high_carbon_grid.csv | 补350年、2.81Gt同一限额下251/528/0个候选对照；说明不可外推LCA；关联：supplemental三情景 | 待两人确认 / OPEN |
| Q5 Results / Letter | P1 | 问题重述要求一页信，当前英文稿未见独立信；段55、175–177、原题p2 | 按教师适用要求补一页机构信，列预算/期限/水安全/环境条件和采取行动前提；关联：67.643T/1036.30y、85.384T/303.99y | 待两人确认 / OPEN |
| Sensitivity Analysis | P1 | 现稿仅定性概述部分因素，缺被测范围与阈值表；表7、段168、173 | 列输入范围、固定/重新选择、可行数/策略切换、影响机制，保留已运行范围；关联：sensitivity_v9.csv、三电网表 | 待两人确认 / OPEN |
| Model Validation | P1 | 新版LP/config guard尚未写入论文；跨平台ID不稳定；新版9条命令退出0；六表无超容差数值差 | 补验证表：算术/服务小例/约束/LP/复现分别支持什么；技术校验与现实验证分开；关联：share_lp_check_v9.json、independent_v9.json | 待两人确认 / OPEN |
| Strengths and Limitations | P2 | 已有局限较清楚，工程边界须与推荐同步；段184–193 | 保留外部服务、寿命、价格、环境代理限制；补179000歧义与有限目录/跨环境ID边界；关联：proofs/audit_scope_v9.md | 待两人确认 / OPEN |
| Managerial Implications | P2 | 有条件行动表，但采购/容量扩张门槛可更具体；表8、段175–177 | 优先列容量可接受性与服务商就绪验证，再列各约束下方案；不把充分上界当预测；关联：Q4/Q5联合筛选63组 | 待两人确认 / OPEN |
| Conclusion | P1 | 缺独立收束段；Main Findings不能替代所有交付要求；段179–193 | 补对五问的简洁回答及条件、未解决项；摘要/结论与新表逐项对应；关联：Q1–Q5证据链 | 待两人确认 / OPEN |
| References | P2 | 六条文献已找到一手页面；全文支持性未全部核验；段196–201 | 核对作者、日期、版本、正文引用；NASA NTP概念上限不能作为设备已实现证据；APA以教师规则为准；关联：review/reference_check.md | 待两人确认 / OPEN |
| Appendix / Reproducibility | P1 | 缺统一可复现附录和新版LP说明；新版run_record与复现清单 | 补版本哈希/入口/依赖、关键算法、LP核验与数据字典；不粘贴全部大JSON；关联：复跑程序/00_运行说明.md | 待两人确认 / OPEN |
| Contents / Figures / Equations | P1 | 目录旧章节、公式旧5.4/5.5、中文待删注、表8.1重号；段9–48、60/62/64/85、149/161 | 统一自动目录与交叉引用，保留有效内容；五PNG/SVG均有新版，不按哈希变化推断数值变化；关联：最新10图文件 | 待两人确认 / OPEN |

P0/P1 在提交前必须解决或取得明确课程处置依据；未取得教师Rubrics不能给Excellent分数。审阅采用 academic-writing-skills 四遍、paper-review 形式符号与计算模块、ARS 方法/主张边界提示；不声称多视角是多位独立人类审核。尚未全面完成 DOCX 视觉渲染、所有数学证明的形式验证和引用全文支持性审查。
