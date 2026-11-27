---
name: or-latex-typesetting
description: Prepare and audit LaTeX equations, notation, tables, floats, references and PDF builds for an existing OR report; does not authorize rewriting research.
---

# or-latex-typesetting

先读[OR适配](../../report-knowledge/OR_ADAPTATION.md)和[排版契约](references/typesetting.md)。沿用现有课程模板；缺模板时只构建独立能力样张，不把样张的页边距/字号当BA2023要求。正式正文改稿另按用户授权。

现有全局math-modeling/tools/latex提供doctor/init/bind/build/validate，正式项目按其generic课程配置调用，不能套CUMCM页数/匿名/图数。其latexmk/XeLaTeX/Biber门禁与本地Tectonic样张验证分开记录。

本Skill资产 assets/capability_fixture.tex 仅合成排版测试，含公式、跨页符号表、三线表、图布局、层级、页眉页脚和BibTeX，不含OR研究数据。用现有引擎隔离编译、记录源/PDF哈希、最终日志及字体/页数、实际渲染后才认定所测能力可用。Tectonic缓存写项目.tools，使用--untrusted；禁止shell escape及自动安装不明宏包。

编译前后调用scripts/latex_audit.py；静态通过不等于编译/视觉通过。依赖路径由宿主工具定位，具体可用性看review/report_skill_migration.md。BibLaTeX/Biber需单独检测，不用BibTeX成功代替。
