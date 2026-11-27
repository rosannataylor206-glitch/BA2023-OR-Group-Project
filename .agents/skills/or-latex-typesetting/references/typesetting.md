# LaTeX排版契约与一手资料

1. **公式与符号**：amsmath的align/aligned/split处理对齐及长式，cases处理分段；避免$$、手工编号和eqnarray。变量斜体，算子用operatorname，物理单位正体；向量/矩阵的粗体规则一致。每式前交代用途，后给条件/量纲/解释；过长式分解时保留数学意义。[AMS math](https://ctan.org/pkg/amsmath)。
2. **三线表/跨页表**：booktabs的toprule/midrule/bottomrule，无装饰性竖线；表头定义单位，误差/区间说明口径。longtable放在正文流，不包table浮动体；设置firsthead/head/foot/lastfoot，续页重复列头，避免拆分行语义。longtable与双栏版式不兼容时改用课程允许的单栏附录，不暗换文档类。[booktabs](https://ctan.org/pkg/booktabs)、[longtable](https://ctan.org/pkg/longtable)。
3. **图表布局**：优先矢量PDF/SVG转换副本或足够分辨率PNG；不改原结果文件。全宽/单栏/双面板按阅读关系决定，固定轴/单位/图例，图题说明情景、筛选与基准；不能将阶梯前沿解释成连续可行集合。避免用缩放字体掩盖过宽图表。缩至正式尺寸检查，再查灰度。
4. **层级/留白/页眉**：用section/subsection语义层级，减少手工vspace、分页及H强制浮动；页面几何、行距、字体和页眉由教师模板确定；调整后重查溢出/空白页/页眉重叠。样张的A4/25mm/11pt仅测试设置。
5. **引用**：label放在caption或编号环境正确位置，用ref/eqref，禁止手输序号。加载hyperref并查重复目标；cleveref仅在模板兼容时用。[hyperref](https://ctan.org/pkg/hyperref)。
6. **BibTeX/BibLaTeX**：一次只选一套后端；bib字段先按一手出版源核实，保持固定cite key。BibTeX/natbib与biblatex/biber分开构建，记录后端版本，未引用/缺条目/重复key均检查。[BibLaTeX](https://ctan.org/pkg/biblatex)。不能虚构DOI、作者或奖项。
7. **字体**：fontspec用于XeTeX/LuaTeX系；字体确实可用且允许嵌入才使用，缺字体明确失败，不静默替换课程指定字体。数学字体与正文协调；检查Missing character与PDF嵌入/替换。[fontspec](https://ctan.org/pkg/fontspec)。
8. **构建质量**：清空隔离构建目录，关闭shell escape，迭代到交叉引用稳定。保留最终log/aux/bbl/PDF和哈希。未定义引用、引用key、重复label、缺字/字体、Overfull均需处置；Underfull逐项目视说明，不全局忽略。确认总页数/正文页数、图表可读、目录准确、书签、超链接、空白页和元数据。Tectonic样张成功不替代完整latexmk/Biber环境。

原包知识来源状态见[OR适配](../../../report-knowledge/OR_ADAPTATION.md)；本文件的一手页面于2026-11-28访问。仅存笔记/链接，不再分发包文档全文或字体。
