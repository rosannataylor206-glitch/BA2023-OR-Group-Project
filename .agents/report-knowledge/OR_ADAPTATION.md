# BA2023 Report Skills适配与来源边界

来源仓库研究分支固定提交fcbe3c2eda3bff0ac1b7c4a4bbba3d32ddba0b65；8个Skill完整目录由官方skill-installer的校验/复制实现迁移，再做路径和课程适配。原仓库和全局配置只读。

## 使用范围

当前只建设Skills/知识库/依赖，不改模型、参数、实验、结论或Report正文。后续以现有研究为对象，核查数学表达、证据、发现与管理价值；不默认重新建模，不以“创新”强行换模型。A类：可复算/可定位的数学或实验错误；B类：有明确价值/成本/验收的补充研究；C类：表达/排版改进。A/B建议先提供来源、影响、成本、验证，重大调整由研究负责人决定。

## 来源继承规则

- 手册分析为来源作者的历史阅读记录；“已读/已目视/未复现/奖项未知”仍属来源状态，本项目没有因此获得相同验证。样本加粗比例、篇幅、章节结构不是课程规则。
- 知识卡是有出处的二次笔记，不替代Taha指定版本或原定理。方法适用才加载：OR以优化/量纲/服务证书为先，不机械引入分类/交叉验证。
- 不复制亚太杯C题数据、模型、实验结果、q1_lock、任务/身份/项目状态。原Skill中的“模拟迁移实验”链接在本项目转为本说明，不导入其结果。
- 独立审核需真实未参与产物的审阅者并绑定SHA；同一Agent自检不是独立验收。人工作者身份不冒署，不强制Michael/tyr身份、不增加竞赛式分工或状态文件。
- 旧手册工具固定441页与特定页范围，仅用于合法原手册复验，禁止拿它们审计OR Report并宣称通过；通用PDF/LaTeX质量检查使用新增QC工具。
- 原截图/原手册PDF不在固定提交中；详见[SOURCE_GAPS](SOURCE_GAPS.md)。不复制教材/论文全文、字体或不明权利资源；本地迁移不自动授权Public再分发。

## 能力路由

LaTeX/表图/符号→or-latex-typesetting；Report结构→or-report-structure及既有academic-writing-skills；数学解释→or-mathematical-exposition；审稿→apmcm-paper-review及既有paper-review；终检→or-report-final-qc。Scientific Visual Design复用apmcm-visualization与全局figure工具；Literature/Citation复用academic-research-suite和其原始来源核验。仅按实际任务加载。

## 共享版补充（2026-11-28）

本套12个Report Skill已按用户明确授权共享至OR仓库；仓库当前保持Public。此授权范围不包含优秀论文PDF、渲染页面或全文提取。源仓库及全局Skills仍只读，不继承其研究事实。

首次使用请读[组员同步与调用说明](../REPORT_SKILLS.md)。所有路径相对本仓库；原AGENTS中的本机绝对路径与历史环境结果仅适用于原机器，不能当新机器依赖已安装的证据。本共享包的SKILL.md及references/scripts/assets均保留。

最新真实获奖论文研读入口为[INDEX](../../references/mcm_outstanding_papers/INDEX.md)，以及同目录PAPER_REVIEW、WRITING_GUIDELINES、VISUALIZATION_GUIDELINES、REPORT_RESTRUCTURE_PLAN。写作、摘要、结构、视觉和数学表达优先按任务读取这些最新成果；原handbook笔记是补充历史资料，不能覆盖本次已核实身份和实际阅读范围。五份文件保留原内容；其中本地PDF/图片/来源原始证据链接在共享版不提供，可沿公开来源链接查阅。

全局operations-research、academic-writing-skills、paper-review、academic-research-suite及math-modeling工具属于可选扩展，不随本次共享安装；不存在时使用当前Skill与本库规范完成其明确支持的范围，需要专门工具或额外方法时如实说明缺口。一般阅读/写作规划不需要Python或完整TeX环境。调用本地脚本才按requirements-report-tools.txt在项目隔离环境安装；TeX编译器、BibTeX/Biber与可视化库按需要另查，不静默安装。

后续正式改稿或研究修正仍遵循用户当轮授权与AGENTS边界。本次仅同步，不触发改稿、模型重建、实验、质量门禁或独立审核。
