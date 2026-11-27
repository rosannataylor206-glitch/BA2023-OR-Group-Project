---
name: apmcm-independent-review
description: "对固定版本的OR Report及相关证据执行真实独立审阅，记录非作者身份、范围与复验条件。"
---

> **BA2023适配优先**：先读 [OR适配与证据边界](../../report-knowledge/OR_ADAPTATION.md)。保留既有模型与实验，按需审查其数学表达；不自动重新选型、跑新实验或改Report正文。原文的“竞赛/队员/根目录状态文件”按课程与双人Report协作解释，不能导入源项目事实。


先完整读取 [共同研究规范](../apmcm-research-philosophy/SKILL.md) 和根目录 AGENTS.md。
确认审核者不是作者，记录身份、PR 和 commit；读取任务验收标准和 HANDOFF。独立复核数学条件、数据处理、代码、复现实验与结论，不以作者总结代替检查。
报告每项问题的文件或公式、依据、实际影响、严重程度、修复方案和通过条件。结论只能为 APPROVED、CHANGES_REQUESTED、BLOCKED。重大错误退回修改，证据或访问缺失说明阻塞；无重大问题且标准满足则批准。
提交 review/ 下绑定commit的审核记录，更新已有Review Matrix，交两名作者确认；不强制新建原仓库的状态文件。禁止作者自批、伪造第二 Agent 审核或依赖未审核核心结果。

[数学迁移验收](../../report-knowledge/OR_ADAPTATION.md)。先独立复现关键数值和数学条件；只有核验所绑定的提交通过后才能按流程作正式判断。
