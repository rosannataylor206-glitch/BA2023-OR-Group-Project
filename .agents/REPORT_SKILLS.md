# Report Skills：组员同步与调用

本次仅共享12个Report Skill、必要引用资源及五份已完成研读文档。用户已明确授权在现有Public仓库发布这些内容；未公开26篇PDF、191个目视页面或全文提取。未检查/整理另外两套既有写作审稿Skill或其他全局Skills。

## 1. 获取完整项目

首次获取（仓库现为Public，无需在聊天中提供Token）：

```sh
git clone https://github.com/rosannataylor206-glitch/BA2023-OR-Group-Project.git
cd BA2023-OR-Group-Project
```

已有克隆：先`git status`保存自己的改动，再执行`git fetch origin`。工作树干净且本地main没有独立提交时，切到main后运行：

```sh
git switch main
git pull --ff-only origin main
```

`--ff-only`拒绝分叉，不覆盖另一人的工作。若Word有未提交改动，先保留独立副本/分支再同步，不用reset --hard或force push。main是共用资料入口，正文改稿仍另建分支/Word副本。

## 2. Codex项目级发现

在Codex中打开克隆后的**仓库根目录**。Skill入口位于`.agents/skills/<skill-name>/SKILL.md`，保留相对引用的`.agents/report-knowledge/`，不要只拷SKILL.md或只下载五份文档。目录不是全局安装，无需复制到个人`~/.codex/skills`。

同步完成后在该项目发起下一轮请求，让Codex重新发现项目Skill；如果菜单尚未显示，可直接指定下列相对入口，先读取再执行。实际桌面菜单是否即时刷新取决于客户端，不能仅凭文件存在宣称另一台机器已加载。

| Skill名称 | 明确用途 |
| --- | --- |
| apmcm-research-philosophy | 研究证据、数学严谨与建设性批评 |
| apmcm-academic-writing | 正文论证和方法/证据一致性 |
| apmcm-abstract | 已核验结果的摘要组织 |
| apmcm-visualization | 图表论证与视觉检查 |
| apmcm-paper-review | 全文结构、主张及证据审阅 |
| apmcm-model-validation | 已有模型的验证范围与证据 |
| apmcm-model-selection | 现有模型选择的理论依据 |
| apmcm-independent-review | 固定版本、真实非作者独立复核 |
| or-latex-typesetting | 数学、表图、引用与TeX构建质量 |
| or-report-structure | 课程问题与章节/证据映射 |
| or-mathematical-exposition | 变量、单位、条件与推导解释 |
| or-report-final-qc | 冻结候选稿的终检 |

## 3. 可直接发送给Codex的请求

```text
使用 $or-report-structure 和 $apmcm-academic-writing。
先读取 .agents/report-knowledge/OR_ADAPTATION.md，以及
references/mcm_outstanding_papers/ 下的五份研读文档。
依据现有Report和课程原件提出章节修改方案，仅做只读分析，不改正文。
```

```text
使用 $apmcm-visualization，参考 VISUALIZATION_GUIDELINES.md，
检查指定图表在最终报告尺寸下的单位、图例、对比与证据来源；先给建议。
```

```text
使用 $or-latex-typesetting 和 $or-mathematical-exposition，
只审核指定LaTeX源的公式、符号、交叉引用与布局，不更改模型或数值。
```

若显式名称不可用，改为“读取`.agents/skills/or-report-structure/SKILL.md`并按其要求执行”。不同任务按需加载，避免每次读取全部12个Skill。独立审阅不能由同一作者/同一Agent假扮第二人批准。

## 4. 最小依赖与工具边界

阅读五份Markdown、进行结构/语言建议不需要安装依赖。只有运行PDF/校验脚本时，选择本机合适的Python建立项目隔离环境；以下命令仅做环境初始化，不是研究复跑：

macOS/Linux（已安装Python 3.11/3.12时，可用其明确解释器路径替换python3）：

```sh
python3 -m venv .venv
./.venv/bin/python -m pip install -r .agents/report-knowledge/requirements-report-tools.txt
./.venv/bin/python .agents/skills/or-report-final-qc/scripts/pdf_qc.py --help
```

Windows PowerShell（已有Python 3.12）：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .agents/report-knowledge/requirements-report-tools.txt
.\.venv\Scripts\python.exe .agents/skills/or-report-final-qc/scripts/pdf_qc.py --help
```

最小工具依赖为PyYAML与PyMuPDF，版本见该requirements；本轮未替组员安装或验证其机器。LaTeX静态脚本只用标准库；真实编译还需本机TeX与对应文献后端。publication_plots示例另需NumPy/Matplotlib；原441页手册工具只用于取得合法原PDF后的历史核验，不得用于普通Report并宣称PASS。全局写作/审稿/OR工具是可选扩展，未随本次发布，不要求先安装全部其他Skills。

## 5. 五份资料与本地链接

- `references/mcm_outstanding_papers/INDEX.md`
- `references/mcm_outstanding_papers/PAPER_REVIEW.md`
- `references/mcm_outstanding_papers/WRITING_GUIDELINES.md`
- `references/mcm_outstanding_papers/VISUALIZATION_GUIDELINES.md`
- `references/mcm_outstanding_papers/REPORT_RESTRUCTURE_PLAN.md`

内容与本地研读完成版逐字一致。它们相互引用并保留论文来源外链；PDF、_reading页面和_provenance原始记录未共享，INDEX中SOURCE_AND_ACCESS/BUILD_REPORT也是本地工作记录，故相关本地链接在GitHub不提供。这不是丢失了本次批准的五份文档；不要据此声称自己看过未同步的PDF或页面。

本目录后附本次逐项提交清单；不包含原Report、模型、代码、研究结果、管理进度文件或其他已安装Skill。正式论文修改另按两位作者确认范围进行。

五份文档中的“仅本地/未上传”是形成当时的历史状态；本次按用户新授权只共享五份笔记与指定Skill，不改变PDF和页面的本地保留边界。

## 本次提交逐项清单

- `.agents/REPORT_SKILLS.md`
- `.agents/report-knowledge/OR_ADAPTATION.md`
- `.agents/report-knowledge/RESEARCH_CRITIQUE_PROTOCOL.md`
- `.agents/report-knowledge/SOURCE_GAPS.md`
- `.agents/report-knowledge/examples/publication_plots.py`
- `.agents/report-knowledge/migration_manifest.json`
- `.agents/report-knowledge/requirements-report-tools.txt`
- `.agents/report-knowledge/research/handbook/ABSTRACT_ANALYSIS.md`
- `.agents/report-knowledge/research/handbook/ABSTRACT_METRICS.json`
- `.agents/report-knowledge/research/handbook/ABSTRACT_VISUAL_AUDIT.md`
- `.agents/report-knowledge/research/handbook/DATA_ANALYSIS_SELECTION.md`
- `.agents/report-knowledge/research/paper_reports/DATA_ANALYSIS_CASES.md`
- `.agents/report-knowledge/research/paper_reports/HANDBOOK_STRUCTURE_AND_MODELS.md`
- `.agents/report-knowledge/research/paper_reports/HANDBOOK_VISUAL_AND_LOGIC.md`
- `.agents/report-knowledge/research/paper_reports/HB-2025-B.md`
- `.agents/report-knowledge/research/paper_reports/handbook_structure_evidence.json`
- `.agents/report-knowledge/research/textbook_cards/KKT_CONDITIONS.md`
- `.agents/report-knowledge/research/textbook_cards/LEARNING_OBJECTIVE_AND_VALIDATION.md`
- `.agents/report-knowledge/research/textbook_cards/OPTIMIZATION_MAP.md`
- `.agents/report-knowledge/research/textbook_cards/RIDGE_REGRESSION.md`
- `.agents/report-knowledge/research/textbook_topics/AI_PROBABILITY_AND_DECISIONS.md`
- `.agents/report-knowledge/research/textbook_topics/AI_SEARCH_AND_SEQUENTIAL.md`
- `.agents/report-knowledge/research/textbook_topics/DIMENSIONALITY_CLUSTERING_AND_EVALUATION.md`
- `.agents/report-knowledge/research/textbook_topics/INDEX.md`
- `.agents/report-knowledge/research/textbook_topics/NONLINEAR_MACHINE_LEARNING.md`
- `.agents/report-knowledge/research/textbook_topics/OPTIMIZATION_THEORY.md`
- `.agents/report-knowledge/research/textbook_topics/REGRESSION_AND_STATISTICAL_INFERENCE.md`
- `.agents/report-knowledge/research/textbook_topics/STATISTICAL_LEARNING_AND_GENERALIZATION.md`
- `.agents/report-knowledge/templates/NOTATION.md`
- `.agents/report-knowledge/templates/workflows/fusion.svg`
- `.agents/report-knowledge/templates/workflows/parallel.svg`
- `.agents/report-knowledge/templates/workflows/prediction-decision.svg`
- `.agents/report-knowledge/tests/learning-objective.test.mjs`
- `.agents/report-knowledge/tools/abstract_audit.py`
- `.agents/report-knowledge/tools/paper_structure_audit.py`
- `.agents/report-knowledge/tools/scan_handbook.py`
- `.agents/skills/apmcm-abstract/SKILL.md`
- `.agents/skills/apmcm-abstract/references/HANDBOOK_EVIDENCE.md`
- `.agents/skills/apmcm-academic-writing/SKILL.md`
- `.agents/skills/apmcm-independent-review/SKILL.md`
- `.agents/skills/apmcm-model-selection/SKILL.md`
- `.agents/skills/apmcm-model-validation/SKILL.md`
- `.agents/skills/apmcm-paper-review/SKILL.md`
- `.agents/skills/apmcm-research-philosophy/SKILL.md`
- `.agents/skills/apmcm-visualization/SKILL.md`
- `.agents/skills/or-latex-typesetting/SKILL.md`
- `.agents/skills/or-latex-typesetting/agents/openai.yaml`
- `.agents/skills/or-latex-typesetting/assets/capability_fixture.tex`
- `.agents/skills/or-latex-typesetting/assets/references.bib`
- `.agents/skills/or-latex-typesetting/references/typesetting.md`
- `.agents/skills/or-latex-typesetting/scripts/latex_audit.py`
- `.agents/skills/or-mathematical-exposition/SKILL.md`
- `.agents/skills/or-mathematical-exposition/agents/openai.yaml`
- `.agents/skills/or-mathematical-exposition/references/exposition.md`
- `.agents/skills/or-report-final-qc/SKILL.md`
- `.agents/skills/or-report-final-qc/agents/openai.yaml`
- `.agents/skills/or-report-final-qc/references/release.md`
- `.agents/skills/or-report-final-qc/scripts/pdf_qc.py`
- `.agents/skills/or-report-structure/SKILL.md`
- `.agents/skills/or-report-structure/agents/openai.yaml`
- `.agents/skills/or-report-structure/assets/section_evidence.csv`
- `.agents/skills/or-report-structure/references/structure.md`
- `.gitignore`
- `references/mcm_outstanding_papers/.gitignore`
- `references/mcm_outstanding_papers/INDEX.md`
- `references/mcm_outstanding_papers/PAPER_REVIEW.md`
- `references/mcm_outstanding_papers/REPORT_RESTRUCTURE_PLAN.md`
- `references/mcm_outstanding_papers/VISUALIZATION_GUIDELINES.md`
- `references/mcm_outstanding_papers/WRITING_GUIDELINES.md`
