---
name: apmcm-model-validation
description: 在数学一致性、数据质量、模型诊断、稳健性和复现实验时使用。
---

> **BA2023适配优先**：先读 [OR适配与证据边界](../../report-knowledge/OR_ADAPTATION.md)。保留既有模型与实验，按需审查其数学表达；不自动重新选型、跑新实验或改Report正文。原文的“竞赛/队员/根目录状态文件”按课程与双人Report协作解释，不能导入源项目事实。


先完整读取 [共同研究规范](../apmcm-research-philosophy/SKILL.md) 和根目录 AGENTS.md。
由研究主张反推验收指标，检查公式、量纲、数据泄漏、边界条件和求解状态。设计基准、消融、外样本验证和敏感性实验，固定数据版本与随机性。保存原始指标和命令，区分已执行结果与待执行计划；测试能运行不代表数学成立。

按需查阅 [STATISTICAL_LEARNING_AND_GENERALIZATION](../../report-knowledge/research/textbook_topics/STATISTICAL_LEARNING_AND_GENERALIZATION.md) 与 [REGRESSION_AND_STATISTICAL_INFERENCE](../../report-knowledge/research/textbook_topics/REGRESSION_AND_STATISTICAL_INFERENCE.md)。先记录部署单位和待验证假设，再选择证据链。

[合成迁移实验](../../report-knowledge/OR_ADAPTATION.md)。按观测依赖选择验证，区分作者复现与独立审核。实际运行，报告精确条件和结果。
