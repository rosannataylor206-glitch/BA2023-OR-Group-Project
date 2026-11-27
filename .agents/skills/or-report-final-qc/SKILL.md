---
name: or-report-final-qc
description: "Run bounded release checks on the exact OR report candidate: source/result provenance, references, PDF layout, metadata and unresolved research issues."
---

# or-report-final-qc

先读[OR适配](../../report-knowledge/OR_ADAPTATION.md)和[终检清单](references/release.md)。终检绑定正文/代码/表图/源/PDF的SHA及运行批次；任何关键改动使相关检查失效。复用paper-review及academic-writing-skills，原手册专用工具不得用于本Report验收。

scripts/pdf_qc.py检查PDF可解析、页数、页尺寸、文本可提取及越界文本候选；结果只是机器证据，不替代逐页目视和数学检查。LaTeX标签/引用/告警用or-latex-typesetting/scripts/latex_audit.py检查。所有工具只读输入，输出写review。

课程门禁与Skill能力测试分开。没有真实Rubrics、必需验证未运行或A类错误未闭合时，不签发提交就绪；C类偏好不得伪装数学错误。真正独立审阅需未参与编写的审阅者，禁止同Agent模拟另一人批准。
