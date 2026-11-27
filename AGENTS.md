# AGENTS.md — Operations Research Group Project


## Project Context

- Course: BA2023 Operations Research
- Project type: Undergraduate Operations Research Group Project
- Current stage: First Draft Baseline Archived / Quality Assurance Review
- GitHub purpose: 两名论文作者统一的资料共享、英文Report版本管理、质量审核及进度同步平台；Public，组员已由用户邀请，Agent不管理成员权限。
- Existing deliverables: Mathematical models, source code, datasets, computational results and academic report.

## Source of Truth

审核依据按照以下优先级执行：

1. 老师发布的 Group Project Guidelines 与原始题目
2. Course Rubrics
3. Course Syllabus 与 Lecture Slides
4. Hamdy A. Taha, Operations Research: An Introduction, 10th Edition
5. 项目数据、数学模型、源代码及实际运行结果
6. 经核实的外部学术文献

若资料之间存在冲突，必须明确记录，不得擅自决定。列入本表不代表资料已取得或已核验；缺失或版本不明时标记“尚未验证”，不得以低优先级来源自行填补高优先级要求。

## Skill Routing

- Mathematical formulation: math-modeling, operations-research
- Data validation: data-analysis
- Algorithm implementation: operations-research and relevant computational skills
- Academic research: academic-research-suite
- Academic writing: academic-writing-skills
- Independent peer review: paper-review
- Specialized analytical skills: Activate only when relevant.

具体入口与按需加载规则见下文“Skills 路由与加载”。采用 paper-review 不自动证明审核具有独立性；最终独立审核须说明审阅者与被审产物的关系及实际核验范围。

## Review Principles

- Mathematical correctness before complexity.
- Computational evidence before claims.
- Reproducibility before presentation.
- Business interpretation before unnecessary innovation.
- Course requirements before competition conventions.

## Non-negotiable Rules

- 禁止捏造数据、实验结果、参考文献或求解器输出。
- 不得为了改善结果而擅自调整原始数据、约束条件或参数。
- 不得将可行解、局部最优解或启发式算法结果直接宣称为全局最优解。
- 未经实际运行或独立验证，不得宣称代码及模型已经通过测试。
- 审核阶段禁止覆盖初稿及原始成果。
- 所有问题必须给出文件位置、证据、严重程度及修复建议。
- 重大模型调整需要获得人工确认。
- 保持数学模型、程序实现、数据、图表和论文结论之间的一致性。
- 遵守课程关于 AI 使用、学术诚信和引用的规定。

## Quality Gates

| Gate | 名称 | 审核范围 |
| --- | --- | --- |
| Gate 1 | Mathematical Model Validation | 问题覆盖、变量/目标/约束、假设、量纲、可行性与最优性适用范围 |
| Gate 2 | Code Correctness and Reproducibility | 实现与公式、输入哈希、环境/依赖、复现命令、实际退出码与独立检查 |
| Gate 3 | Numerical Results and Sensitivity Analysis | 数值精度、约束残差、边界案例、基准对照、敏感性及解释范围 |
| Gate 4 | Model–Code–Paper Consistency | 数据→模型→代码→结果→表图→正文/摘要的数值、符号、单位与主张一致性 |
| Gate 5 | Academic Writing and Course Rubric Review | 学术表达、引用支持、结构/格式、业务解释与课程评分标准覆盖 |
| Gate 6 | Final Independent Review | 对冻结候选版本作最终独立复核，记录遗留问题与提交建议的适用范围 |

每道门禁须记录受检版本/哈希、依据、执行者、检查方法、证据、状态和未解决项。未执行记 NOT_RUN，证据不足不能标记 PASS。上述课程门禁不等同于 math-modeling 的 M1/P1/P2/W1/W2，不得相互替代或借用历史通过状态。

所有重大问题必须被解决或明确披露，才能建议进入最终提交阶段。明确披露不自动等于课程允许保留，也不免除必须修复的问题；不确定时记录并交由人工判断。

## Output Requirements

- 所有审核报告统一存放在 `review/` 目录。
- 审核报告使用中文，保留必要的英文专业术语；正式学术报告中的英文修改建议使用英文。
- 所有结论必须区分“已验证”“存在风险”与“尚未验证”，并注明证据和验证范围；“存在风险”的判断也须区分已确认问题与待核实线索。


## 项目身份与当前边界

- 本项目是 BA2023 Operations Research 本科课程小组项目。用户确认建模、编程求解和论文初稿已完成，下一阶段为全面审核。
- Phase 1 已获批准并完成私有基线存档；远程与原始 README 父提交、95 文件和 Tag 已逐项核验。基线存档后，用户已授权连续开展 Phase 2–5 的环境准备、真实复跑与独立审核，无需逐个小步骤确认。正式修改数学模型、核心代码与论文须先交综合审核报告和整改方案，再获人工确认。
- 审核依据按照下文 Source of Truth 执行；不得将竞赛规则当作课程规则。
- 当前仅发现文件名为 `队友已完成初步/3. BUS2003_Group Assignment Guideline.docx` 的课程材料，BA2023 的字数、格式、提交方式、AI 披露和评分标准尚未核验。不得自行套用 BUS2003 或 CUMCM/APMCM 的要求。
- 根目录 `report.1docx.docx` 是候选初稿；`MCM_B_v9_编程组/` 是候选编程交付；`MCM_B_v9/`、`MCM_B_v6/` 和 `output/` 包含多版本及交接副本。正式审核开始时先建立权威文件清单，不得仅凭版本号或修改日期认定唯一权威。
- `2026 MCM B 2/` 含另一套 CUMCM 题目与 XLSX 附件，不得自动并入月球基地模型或论文证据。

## Skills 路由与加载

全局 Skills 直接复用 `/Users/Rosanna/.codex/skills/`，只读，不复制重复版本。每次实际执行某类任务前读取对应入口和当阶段需要的参考，不一次加载整套资料。

| Skill | 入口 | 后续用途 |
| --- | --- | --- |
| operations-research | `/Users/Rosanna/.codex/skills/operations-research/SKILL.md` | 目标、变量、约束、可行性、最优性范围、敏感性审核 |
| math-modeling | `/Users/Rosanna/.codex/skills/math-modeling/SKILL.md` | 建模—程序—论文证据链、角色分工、阶段验证 |
| data-analysis | `/Users/Rosanna/.codex/skills/data-analysis/SKILL.md` | 数据来源、口径、单位、结果表和图表溯源 |
| academic-writing-skills | `.agents/skills/academic-writing-skills/SKILL.md` | 论证、方法与证据一致性、学术表达、跨材料完整性 |
| paper-review | `.agents/skills/paper-review/SKILL.md` | 只读全面评审、定位问题、严重度、修订边界 |
| academic-research-suite | `/Users/Rosanna/.codex/skills/academic-research-suite/SKILL.md` | 按需补充方法审稿、引用核验、反例检查；不重复整套评审 |

- 项目级两个 Skill 从 `/Users/Rosanna/Documents/GitHub/CUMCM/.agents/skills/` 完整复制；不得覆盖或改写历史源。标准 `.agents/skills/` 位置和上述入口均可供显式读取，本会话后续 Skills 更新已列出这两个项目级入口；目录可读与客户端菜单显示仍须区分。
- `paper-review` 以 `academic-writing-skills` 为基础。拟审核模块为形式符号/显示量溯源及计算模型模块，正式审核时依据正文确认。不得因出现“水”字就套用流域、水政策、SEM、洪水或特定实验室审稿偏好。
- `pymoo`、`statsmodels`、`scikit-learn`、`scikit-survival` 当前不启用。现有数值代码使用 NumPy/SciPy、物理积分、优化与有限目录筛选；多目标权衡并不自动要求进化算法，故障分析也不自动等于删失生存分析。只有确认对应方法实际存在或获准新增时才读取。
- DOCX/PDF/XLSX 操作分别读取全局 `math-modeling/tools/docx/SKILL.md`、`tools/pdf/SKILL.md`、`tools/xlsx/SKILL.md`；有版式交付时另读取适用的宿主文档/PDF/表格 Skill。无 LaTeX 重建任务时不启动 LaTeX 工具。
- 全局存在 math-modeling 的嵌套 dsh-plugin 同名版本，默认使用上表根入口，避免重复触发。

## 课程适配与冲突处理

- Skill 的竞赛默认值不是 BA2023 作业要求：不强制 30 页、20 MB、匿名、15000 字、8 幅图、竞赛摘要结构、固定 AI 声明或 52 个赛前/赛期决策。
- 全局 math-modeling 主入口默认图数不限，DOCX 子工具却写至少 8 幅图，存在内部差异。执行格式校验前按已核验课程要求配置，并记录参数和依据，禁止以凑图或降标准掩盖失败。
- 本轮只检查这些协议，不调用初始化脚本生成 `contest_setup.json`、根目录竞赛台账、证据链、决策日志或任何模型/论文固定交付物。保留已有同类文件。
- 后续若明确采用 math-modeling 正式流程，需先说明课程适配、模式、适用门禁、责任人及 Skill 限制。`deep` 需显式启用，不能因“已有初稿”自动切换，也不得把旧输出中的 PASS 当作本轮通过。
- ARS 默认 inline 角色提示词，不启用 hooks、跨模型上传或后台团队；math-modeling 的独立质检仅在正式阶段确实适用时使用。当前环境配置不触发 M1/P1/P2/W1/W2。任何未运行的独立验收均记 NOT_RUN，不伪称 PASS。

## 基线存档后的全面审核工作流

1. 冻结课程要求、初稿、模型说明、数据、代码、结果和交接包的权威版本与 SHA-256；列出缺失和相互冲突的材料。
2. 模型审核：逐题核对决策变量、目标、约束、量纲、假设、参数来源、物理/工程边界、可行性和所谓最优性的适用范围。
3. 程序审核：先静态检查，识别所有写文件副作用。复跑只在 `review/` 下完整隔离副本执行，不在原目录直接运行 `run_v9.py`、`verify_v9.py`、交接、绘图、打包或建文档脚本。
4. 数据与结果审核：核对输入哈希、随机种子、环境版本、约束残差、守恒、边界案例、独立基准、敏感性及结果表；记录实际命令、退出码、误差和时间。
5. 论文只读审核：论证结构；方法与结果证据；学术表达；交付完整性四遍检查。追踪“问题→模型/代码→输出→表图→正文/摘要”，核验引用真实且支持对应主张。
6. 在 `review/` 输出带章节/页码/文件位置、证据状态、严重度、受影响材料、建议与阻塞阶段的问题清单。缺失、未核验、未运行须分别说明，不编造人工确认。
7. 用户授权修订后另建版本，记录改动及上下游影响。发生实质变化时重新检查受影响项，不覆盖初稿或原始结果。

## 验证与决策要求

- 使用真实运行结果；求解器状态、约束回代与最优性证据分开报告，有限候选目录的最优不得扩张为无条件全局最优。灵敏度或程序复现不能替代外部有效性验证。
- 数值与单位在代码、JSON/CSV、表图、正文和摘要中须一致；明确绝对/相对容差及原因，不靠手动修改报告数字消除冲突。
- decision_log 记选择、理由、责任人和回滚成本；evidence_chain 记主张与来源/程序输出。已有记录先核对后复用，不重新初始化覆盖。高影响方案变更须由用户/组员决定；不得伪造历史选择或以 AI 代替人工核验。
- DOCX 修改须做结构与渲染检查，比较正文、表格、公式、图像与分页；XLSX 须确认表头、首尾行、公式与重算；PDF 须确认页数、文本及图表可读性。检查只对实际检查的版本和范围有效。

## Python 与执行规则

- 不使用含义不明确的 `python`/`python3` 执行业务脚本。环境实测见 `review/00_skill_inventory.md` 与 `review/00_skill_checks.json`。
- 基础数值检查：`/opt/anaconda3/bin/python`（3.12.7），当前 NumPy 1.26.4 不满足 v9 的 `numpy>=2.0`，只能作为基础检查环境，不能声称完整复现环境就绪。
- 文档读取环境：`/Users/Rosanna/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`（3.12.14），具备 DOCX/PDF/XLSX 库，缺 SciPy/Matplotlib。使用前重新调用宿主依赖定位工具，以防更新后路径变化。
- 终端默认 `python3` 是 Python 3.14.0，缺核心数值/文档包。不得混入其他解释器 site-packages，不改变全局 PATH 或升级 Anaconda。
- NumPy/SciPy/Matplotlib 的历史精确版本仅为复现目标；离线可用性、平台兼容性未证明。需要新环境时优先项目隔离环境与可信缓存；不得无差别安装全部 Skill 依赖或从不可信来源安装工具。
- 环境探测禁写字节码（`PYTHONDONTWRITEBYTECODE=1`），绘图库缓存使用临时目录。不得为检查环境而导入会写结果的项目模块。

## 文件边界

- 当前可补充项目管理文档、AGENTS.md、.gitignore 与 review/ 下基线记录；保留有效规则。Phase 1 审批前仅做清单与结构/共享检查；Phase 2–5 在基线存档后执行，新环境和复跑证据均位于项目隔离目录。原始成果仍只读。
- 已有模型、数据、代码、结果、论文和压缩包只读；旧项目、全局 Skills 与用户全局配置只读。不得清理、重命名、迁移、覆盖或自动修复这些文件。
- 配置结束须比较原始文件 SHA-256，报告任何新增、删除或变化；配置就绪不代表论文、模型或结果已通过审核。


## GitHub 协作与持续进度同步

- 唯一目标仓库：`rosannataylor206-glitch/BA2023-OR-Group-Project`，当前按用户最新明确选择保持 **Public**；任何未来可见性调整以用户新指令为准。创建/连接状态见 `review/00_github_setup.md`；未经实际读取验证不得声称仓库已创建或可见性正确。
- `Ma-mj-Mar/CUMCM` 与 `zelin-michael-zhu/apac-competition-2026-11-26` 仅作只读参考，不向其写入、推送、建 Issue 或改变配置。Agent 不代为邀请成员。
- 已有仓库、Projects、原18项阶段 Issues 与标签须保留，不重新创建；用户已选择仓库 Public，已自行邀请一名组员，Agent 不管理成员。可以补充项目管理与审核记录，但不能借整理基线改变原文件路径或代码运行关系。
- 首次推送前必须生成逐项拟上传清单和哈希，取得人工明确确认。不得 `git add .`，不得用 Contents API、Issue 附件或其他上传手段绕过批准。确认范围后才提交初稿基线并建立 `v0.1-first-draft`；Tag 只代表实际纳入文件的初稿快照，不是质量通过证明。
- 默认分支 main 仅存经确认的稳定版本。审核、整改、模型、程序、论文分支分别按 `review/audit`、`review/revision-v2`、`feature/model`、`feature/code`、`feature/paper` 命名；可加 Issue 后缀，仅创建实际需要的分支。
- main 不直接实施未经审核的重大修改；不强制推送、不自动合并重大 PR。新版本须保留原始成果并记录影响范围，重大模型调整须人工确认。
- 本地隐私预检原始记录、带本机绝对路径的环境明细、第三方 Skill、教材/课程资料/题目附件、未知共享权限的数据、工具、缓存、临时文件、压缩副本和大结果文件不自动上传。`.gitignore` 不替代逐项确认，也不能保护已被追踪的文件。
- Projects（如可用）名为 `BA2023 OR Group Project — Progress Board`，须保持私有；状态为 To Do / In Progress / In Review / Done / Blocked。Category 为 Requirements / Environment / Mathematical Modeling / Programming / Data & Validation / Academic Writing / Quality Assurance / Presentation / Final Submission。不可用时以 Issues 与 PROGRESS.md 替代，明确记录限制。
- Issue 严重度标签为 P0-critical / P1-major / P2-minor / P3-enhancement；领域为 modeling / programming / data / paper / validation / documentation，阻碍用 blocked。阶段任务与实际缺陷分开记录，不编造问题；负责人未确认写待认领。
- 每个实际问题记录 Issue ID、描述、严重程度、文件位置、证据、影响范围、修复建议、验证方法、负责人和当前状态。

每次完成一个重要审核阶段或整改任务后：

1. 更新 PROGRESS.md。
2. 更新相关 GitHub Issue。
3. 在有权限时同步 GitHub Projects 状态。
4. 保存审核报告、测试证据和修改记录。
5. 创建具有明确说明的 Git Commit。
6. 在获得相应授权后推送至指定分支。
7. 不得擅自合并未经人工确认的重大修改。
8. 不得将没有验证的任务标记为 Done。

保持 GitHub 进度与真实工作进度一致。只有初稿完成的任务，可记录为“初稿任务 Done、审核 NOT_RUN”，不得将审核任务一并关闭。仓库、Issue 或看板同步失败时更新本地阻碍与待同步清单，不伪称远程已更新。


## 个人研究质量提升：六阶段长期规范（用户最新指令）

最终目标是完善已有建模、编程及论文成果，形成数学严谨、计算可靠、逻辑完整、可复现、具有实际商业决策价值并符合 BA2023 评分要求的英文报告。课程 Rubrics 的 Excellent 档为目标；未取得真实 Rubrics 时不得虚构评分标准、档次描述、权重或分数。借鉴数学建模竞赛的研究严谨性，不为创新而盲目增加模型复杂度。

### Phase 1：初稿基线与唯一确认点

先复核最终上传文件、存储权限、敏感信息与 SHA-256，覆盖模型及推导、完整代码、必要参数/数据、核心结果、实验图表、可编辑论文与审核/管理记录。只选一套现行候选主线；历史重复副本和不相关实验排除，原路径不动。大结果若属于证据依赖不得仅因体积一律删除；在清单说明必要性与存储方式。

**在最终清单展示且用户确认范围和存储权限前停止。** 批准后仅逐项暂存批准文件，核对哈希，首次 Commit、Tag `v0.1-first-draft` 并 Push。Tag 为初稿快照，不表示审核通过；仓库可见性后来由用户明确改为 Public，Projects 保持原可见性。不以 Contents API、Issue 附件等绕过上传审批。

### Phase 2：正式审核准备

读取 AGENTS、Skill Inventory、GitHub Setup 和环境证据。优先建立本项目独立 Python 环境解决 NumPy 等依赖兼容性，不修改其他竞赛环境或全局 Anaconda。核验原始题目、Group Project Guidelines、Rubrics、Syllabus、相关 Slides 与 Taha 第 10 版适用内容；缺失、版本不明或冲突明确列出，不自行补造要求。

### Phase 3：全面独立审核

按需读取已配置的 math-modeling、operations-research、data-analysis、academic-research-suite、academic-writing-skills、paper-review 及当前任务模块。分别从建模专家、算法工程师、数值验证分析师、学术审稿人与课程评审视角检查；多视角自检不得冒称独立复核，实际独立检查须记录审阅者与被审产物关系。适用 Skill 要求独立质检时执行对应门禁，不模拟 PASS。

不得默认模型/代码正确。实际运行可运行程序，并以独立计算、约束代回、小规模测试、边界检验、适用的交叉验证/基准比较检查模型、目标/约束、参数来源、代码实现、可行性、最优性范围、复现与结论证据。不能把无预测任务的交叉验证机械强加给确定性优化。敏感性、情景与对照实验按证据缺口提出；任何会改模型或核心代码的补实验方案先写入整改建议，不直接改原成果。所有复跑在隔离副本执行。

### Phase 4：逐章节论文完善方案

按实际论文逐章给出保留、修改、删除、补充的具体位置、理由、证据及可执行动作，覆盖：数学模型和公式推导的完整性；模型选择的理论依据；结构与论证；缺数据/实验支持的结论；补实验或重算；敏感性/情景/对照；图表重绘或优化；准确、专业、简洁的英文表达；参考文献真实且与正文对应；管理启示与商业决策价值；可能影响课程评分的问题。英文修改建议用英文，审核说明用中文，不限于语言润色。

### Phase 5：七份综合审核交付

- `review/01_model_audit.md`：数学建模审核。
- `review/02_code_audit.md`：编程与算法审核。
- `review/03_results_audit.md`：数据与数值结果验证。
- `review/04_paper_audit.md`：逐章节论文深度审核与完善方案。
- `review/05_consistency_matrix.md`：模型、代码、数据、结果及论文一致性矩阵。
- `review/06_rubric_assessment.md`：按真实课程评分依据评估，缺失项不得评分或声称 Excellent。
- `review/07_master_audit_report.md`：综合发现、阻碍、优先级和可执行整改路线图。

问题分 P0 Critical / P1 Major / P2 Minor / P3 Enhancement，每项记录文件位置、证据、影响、修改建议和验证方法；对应 GitHub 标签仍用 P0-critical / P1-major / P2-minor / P3-enhancement。已验证、存在风险、尚未验证明确区分；缺失材料不伪装成已审阅，未运行不伪装为测试记录。

**正式修改数学模型、核心代码及论文前，必须提交上述综合报告与整改方案，经用户确认后才进入受控整改。** 审核授权不等同于修改授权；不因一个小测试通过就认为整条链正确。

### Phase 6：个人进度与成果同步

每完成重要阶段，保存报告/测试证据，更新 PROGRESS、相关现有 Issues、Projects 和 CHANGELOG，记录明确 Commit，并仅在已批准的上传范围和存储权限内同步 GitHub。新增未批准文件或敏感/第三方内容先补清单再确认；无权上传时保留本地并披露。用户无需逐个小步骤批准已授权的审核，但重大模型、核心代码和论文修改仍受综合方案确认门禁约束。用户已自行邀请一名组员；Agent 不代为邀请或管理成员，不继续扩展复杂多人机制。

## 2026-11-27 可见性与成员最新指令

用户本人曾将仓库改为 Public 并邀请一名组员；此前 Private 规则已被用户最新明确选择覆盖。仓库当前须保持 **Public**，允许公开已上传成果。Projects 的可见性未要求改变，仍保持 Private。未来上传新增文件仍核对权限、敏感性和批准范围；Agent 不更改现有组员邀请/权限。

## Report中心双人协作（2026-11-27 最新指令，覆盖旧角色分工描述）

- 目前只有用户与另一名论文同学参与后续工作；不设建模手/编程手岗位，不按竞赛阶段重新组织人员。Skills作为技术核验与写作审阅方法按需使用，课程要求优先。
- 最新技术候选为 MCM_B_v9 模型/证明与 月球基地_编程组交付包_修订版；已核对源码哈希与默认结果，具体运行批次/限制见 review/latest_sync_report.md。旧 MCM_B_v9_编程组 为v0.1历史基线。
- 最新论文候选仍report.1docx.docx；所有章节改稿按review/report_review_matrix.csv记录问题、证据、优先级、建议、关联模型/结果、负责人和状态，负责人待两人确认。
- 每次更新先读本地/远程分支与commit，登记父版本/SHA、改动、影响、验证及待同步事项。DOCX不得自动合并；并行稿保留独立文件名/分支，人工合并新版本后复核数值与渲染。
- 共用GitHub固定commit获取最新版，不以聊天压缩包替代版本记录。保留v0.1-first-draft及所有有效历史，不force push、不覆盖组员成果。
- 用户已确认共同作者同意公开新增64文件及配套MCM_B_v9研究成果；题面/课程/第三方全文/Skills/个人敏感信息排除。其后新增公开权限不明内容先确认。
- 工作聚焦Report完整性、数学表达、可复现数值/图表、敏感性、管理价值、英文和引用；无实质错误不重建模型或重构代码。重大模型/核心结果变更、正式改稿范围及Word冲突须确认。
