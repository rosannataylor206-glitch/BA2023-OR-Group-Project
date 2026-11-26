# 初稿基线：核心成果与依赖覆盖

本记录只做 Phase 1 存档范围检查，不构成数学、数值或学术审核通过。原路径和内容不变。候选主线为 `MCM_B_v9_编程组/` 与根目录 `report.1docx.docx`；最终范围需用户确认。

| 成果 | 拟保留路径 | 覆盖与限制 |
| --- | --- | --- |
| 英文论文初稿与可编辑源 | `report.1docx.docx` | DOCX 本身为可编辑源；ZIP 完整，可见 416 个段落、8 个原生数学元素、9 个媒体文件。仅结构统计，不证明公式/论文内容正确；未找到同一英文初稿的独立 LaTeX/Markdown 生成源，不以建模 DOCX 生成器冒充 |
| 模型说明与公式 | `MCM_B_v9_编程组/MCM_B_v9_建模修订与独立验证说明.docx` | 479 个段落、20 个原生数学元素、3 个媒体文件；与 MCM_B_v9 下同名文件 SHA-256 相同，只存一份 |
| 数学推导 | `MCM_B_v9_编程组/proofs/` | 8 份 Markdown，含物理、建设、供水、联合方案、成本/环境、敏感性、参考与适用范围 |
| 完整代码 | 编程组根、`reference/`、`utils/` | 共 21 个 PY；静态导入所识别的本地模块均在拟上传集，不导入或执行项目模块 |
| 数据、参数与来源 | 数值代码中的参数/数据类与 `evidence/*.json` | 8 份来源/假设 JSON。README 声明部分值是设计情景而非观测；存档该口径，不将其认定为可靠实测数据。当前静态读取链未显示需要那套无关 XLSX 附件；动态读取完整性仍待实际复跑 |
| 主要数值输出 | `results/physics_v9.json`、`water_v9.json` 等，以及 ZIP 恢复的 `joint_v9.json`、`phases_v9.json` | 保留已有结果；仓库检出后先运行 `python3 review/baseline/restore_large_results.py` 恢复两份证书，不据历史记录宣称本轮通过 |
| 阶段证书 | `results/core_certificates_v9.zip` 内的 `phases_v9.json`、直接存储的 `sensitivity_phases_v9.json` | 与方案的 phase_id / transport_ref 相互引用，不单独删去 |
| 敏感性分析 | `results/sensitivity_v9.json` 与 CSV | 保留已存在分析供后续审核，不假定分析充分 |
| 核心图表 | `figures/` 下 5 PNG + 5 SVG | 保留彩色图及可编辑矢量源；5 份灰度 QA 预览排除，仅本地保留 |
| 审核/复现历史 | `evidence_chain/`、`ai_ledger/`、results 中运行/验证/复现记录 | 原样保存历史主张；后续独立核验，不借历史 PASS 给本轮背书 |
| 本轮管理与检查 | README、AGENTS、PROGRESS、CHANGELOG、CONTRIBUTING、review 配置/本节记录 | 含必要审批与质量规则；本机隐私扫描原始记录和凭证明细不上传 |

## 为什么补充四个大 JSON

- `verify_v9.py:489` 直接读取 joint_v9.json；`:546` 读取 sensitivity_v9.json。
- `plot_handoff.py:62` 读取 phases_v9.json，`:136` 读取 joint_v9.json。
- `registry_v9.py` 负责展开共享阶段/运输证书；方案只存引用时，阶段文件是实际证据的一部分。ZIP 是无损封装，恢复脚本检查原始 SHA-256，执行原代码前必须恢复。
- `programming_handoff.py`、`utils/supplemental_io.py` 和建模 DOCX 生成器还读取方案/结果。

上述行号来自本轮读取的源文件，只证明静态依赖。程序尚未在本轮执行，实际可运行性不能据此认证。

## 保留的外部依赖与缺件

- 独立数值环境尚未建立：NumPy / SciPy / Matplotlib 兼容性将在基线存档后的 Phase 2 解决。
- 建模 DOCX 生成器需要 Pandoc 与字体；不复制许可尚未核验的第三方字体。
- `package_v9.py` 要求 `evidence/2026_MCM_Problem_B.pdf`。其存储授权未确认，因此该 PDF 不在本次远程清单；原打包流程不能被宣称完整就绪。保留本地 PDF 和源代码，未修改或绕过该要求。
- `programming_handoff.py --compare-with ../MCM_B_v9` 是可选跨历史包比较，历史目录不纳入本基线；其历史报告可保存，但该项比较需后续另行提供原档。
- 原英文论文生成链尚未确定，不能承诺由 `build_report_v9.py` 重新生成根目录英文报告；该脚本对应另一份建模说明。
- BA2023 的适用 Guidelines、原始题目、Rubrics、Syllabus、Slides、Taha 第 10 版章节内容目前未核验。目录中 BUS2003 命名材料不自动构成 BA2023 依据；本阶段不编造课程要求。

## 隐私与授权

两份 DOCX 有非空作者元数据；正文、批注、修订、嵌入媒体也可能含作者或第三方信息。用户已确认 95 项存储范围。英文论文上传副本仅移除 WPS 数字账号标识、最后修改者账号和三个应用追踪属性；本地原件未改，正文、批注、图像及作者显示署名保持一致。审计时须同时记录原件与上传副本哈希。
