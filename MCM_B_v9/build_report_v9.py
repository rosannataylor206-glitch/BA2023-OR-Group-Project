"""Build the v9 modeling handoff after independent checks have passed.

The report reads current numerical artifacts, never a hand-entered winner.
The operation marker for this deliverable is owned and already run by root.
"""
from pathlib import Path
from copy import deepcopy
import json, math, re, subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent
AS=ROOT/'report_assets';OUT=ROOT/'deliverables'

def read(name):return json.loads((ROOT/'results'/name).read_text(encoding='utf-8'))
def number(v,d=1):return f'{v:,.{d}f}'
def route(v):return {None:'无运营补给','R':'火箭','E':'电梯接驳','ER':'两路'}.get(v,str(v))
def prep(v):return '火箭' if v==0 else ('电梯接驳' if v==1 else '两路各半')
def water_label(v):
    if v=='stock_all':return '全年预存水'
    rate='98%' if '0.98' in v else '94%'
    if '_ER_' in v:return rate+'回收 两路分区'
    if '_R_2independent' in v:return rate+'回收 火箭两区'
    if '_R_4independent' in v:return rate+'回收 火箭四区'
    if '_R_2flights' in v:return rate+'回收 双火箭整批'
    if '_R_4flights' in v:return rate+'回收 四火箭整批'
    if 'every3' in v:return rate+'回收 电梯每三日'
    return rate+'回收 电梯每两日'


def data():
    J=read('joint_v9.json');P=read('physics_v9.json');W=read('water_v9.json')
    V=read('independent_v9.json')
    if V.get('all_implemented_checks_pass') is not True:
        raise RuntimeError('The independent v9 audit must pass before authoring the final report')
    index={r['id']:r for r in J['candidates']}
    default=[r for r in J['candidates'] if r['mode']=='fault' and r['mission_key']==J['default_mission_key']]
    return J,P,W,V,index,default


def charts(J,index,default):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.2,
        'axes.spines.top':False,'axes.spines.right':False})
    table=J['construction_summary'];fig,ax=plt.subplots(figsize=(7.0,2.55))
    names=['R','E','ER'];xx=list(range(3))
    for mode,shift,color in [('ideal',-.17,'#7B97AB'),('fault',.17,'#D18F40')]:
        vals=[next(z['delivery_upper_years'] for z in table if z['route']==r and z['mode']==mode) for r in names]
        bars=ax.bar([i+shift for i in xx],vals,width=.32,label='Ideal support' if mode=='ideal' else 'Fault support',color=color)
        for b,v in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,v+15,f'{v:.1f}',ha='center',fontsize=8)
    ax.set_xticks(xx,['Direct rockets','Elevator + transfer','Combined routes'])
    ax.set_ylabel('Construction upper time (years)');ax.set_ylim(0,max(z['delivery_upper_years'] for z in table)*1.16)
    ax.legend(frameon=False,fontsize=8);ax.grid(axis='y',alpha=.2)
    fig.tight_layout();fig.savefig(AS/'construction_times_v9.png',dpi=180,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.0,2.75))
    points=ax.scatter([r['habitation_upper_days']/365 for r in default],
        [r['scenarios']['central']['cost_usd']/1e12 for r in default],
        c=[r['construction_E_share'] for r in default],cmap='viridis',s=10,alpha=.38,edgecolors='none')
    frontier=sorted((index[i] for i in J['cost_time_frontier_ids']),key=lambda r:r['habitation_upper_days'])
    ax.plot([r['habitation_upper_days']/365 for r in frontier],[r['scenarios']['central']['cost_usd']/1e12 for r in frontier],color='#A66C26',lw=1.5,label='Saved budget-time frontier')
    ax.set_xlabel('Sufficient inhabitation upper time (years)');ax.set_ylabel('Illustrative budget (USD trillion)')
    cb=fig.colorbar(points,ax=ax,pad=.015);cb.set_label('Construction share via elevator')
    ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=8)
    fig.tight_layout();fig.savefig(AS/'cost_time_v9.png',dpi=180,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.0,2.65))
    for scenario,label,color in [('central','Historical-grid illustration','#567D92'),('low_carbon_grid','Low-carbon grid scenario','#328374')]:
        ids=J['selections'][scenario]['cost_environment_frontier_ids']
        rr=sorted((index[i] for i in ids),key=lambda r:r['scenarios'][scenario]['CO2proxy_kg'])
        ax.plot([r['scenarios'][scenario]['CO2proxy_kg']/1e12 for r in rr],
                [r['scenarios'][scenario]['cost_usd']/1e12 for r in rr],color=color,lw=1.7,label=label)
    ax.set_xlabel('Selected emissions proxy (trillion kg CO2-equivalent)')
    ax.set_ylabel('Illustrative budget (USD trillion)');ax.grid(alpha=.18);ax.legend(frameon=False,fontsize=8)
    fig.tight_layout();fig.savefig(AS/'environment_v9.png',dpi=180,bbox_inches='tight',pad_inches=.12);plt.close(fig)


def blocks(J,P,W,V,index,default):
    pages=[];equations=[]
    def p(s):return ('p',s)
    def eq(s):
        if s not in equations:equations.append(s)
        return ('eq',s)
    def table(h,rows,widths=None):return ('table',(h,rows,widths))
    def pic(name):return ('pic',name)
    def links(rows):return ('links',rows)
    def page(title,*rows):pages.append((title,rows))
    mk=J['default_mission_key'];M=J['missions'][mk]
    chosen=index[J['selections']['central']['min_cost_policy_id']]
    fastest=min(default,key=lambda r:r['habitation_upper_days'])
    stock=min((r for r in default if r['water_id']=='stock_all'),key=lambda r:r['scenarios']['central']['cost_usd'])
    water=J['water_catalogues']['fault_'+mk];water_index={w['id']:w for w in water}
    feasible_water=[w for w in water if w['feasible']]
    modeword={'ideal':'理想支持','fault':'故障支持'}

    page('修订结论与阅读顺序',
        p('v9恢复固定运输能力的原题基准，补入火箭循环补水候选，并把建设期货损、补发和备用船纳入同一质量与时间账。我们比较事先承诺的保守资源预算和工期；目录内最低预算不能直接成为唯一工程推荐，也未证明故障实际发生后的支出最低。'),
        table(['v8的实质遗漏','v9如何落实'],[
            ['回收供水与电梯路线绑在一起','回收率、运营补给路线和初始预置路线分开比较；火箭、电梯和分区联合方案均进入目录。'],
            ['50年截止与运力扩容替代原题基准','三港额定提升能力固定，建设工期作为输出；另给理想与故障基准，50年只作附加期限查询。'],
            ['失败只减少机会，缺少毁损补发账','成功交付扣除货物毁损；全额尝试、推进剂、永久船损备用和首次部署均计入。']],[2.0,5.1]),
        p('本模型还有一个重要前提：顶端仓储和月面机器人接收能力作为2050年前可预订的外部服务。我们核算所需容量与服务费用，服务方设施建造部署的质量和时间尚未进入物理账。因此本轮不是从零建设全部基础设施的闭合工程方案。'),
        p('在声明的固定能力和服务参数下，三种路线得到数百年至千年量级的充分工期上界。这些数值揭示吞吐量与建设规模的关系，不能解释为对未来千年工程进度的预测。'),
        p('建议先读第2至3页的题目与阶段，再读第4至10页的证明路径。第11至16页展示结果及敏感性，第17至19页说明验证、来源和交接，第20页为附条件的机构建议信。'),
        p('本报告是核心建模修订与复现说明。数学保证依赖写明的故障支持、维护就绪条件与服务界；真实硬件性能、长期维护与未来单价仍须工程证据。'))

    page('原题要求与参数身份',
        p('官方题面从2050年开始，要求比较三港电梯系统、传统火箭和联合方式运输约1亿吨材料的成本及工期，研究不完美运行、一年供水与地球环境影响。题面没有50年建设截止日。'),
        table(['输入','当前值','身份'],[
            ['建设材料','100,000,000吨','官方规模基准'],
            ['港口数','3个','官方最终系统'],
            ['每港年提升量','179,000吨','沿用每港额定值解释；提升货物与推进剂的总质量'],
            ['火箭基地','选择10个','来自题列基地；主基准采用全部10个'],
            ['月球单枚净载荷','125吨','题面100至150吨范围内的研究取值'],
            ['每基地发射机会','250次每年','未来服务日历情景，题面未给此频率'],
            ['生活医疗用水','1,154.4吨每天','962吨基线加20%设计余量；非NASA十万人月面实测']],[1.8,1.8,3.5]),
        p('主基准输出仓储、机器人接收和供电所需规模。顶端仓储和月面接收服务必须在首批建设货物到达前可用，其费用为容量预订及服务费用；提供方设施的部署载荷和工期尚未闭合。只有明确的压力情景才施加额外预算。农业、工业及额外冷却用水需要新增水流输入。'),
        p('简单量级核对也排除了50年固定能力目标：按250次每基地每年的情景，即使忽略推进剂、干结构和故障，三港与火箭合计年均最多849,500吨，50年仅42,475,000吨。年均数量下界约117.7年；详细工期更长，是因为还要计推进剂与服务保障。'),
        p('电梯系统在2050年前已建成，因此原有电梯资本不再重复记入本轮增量支出；其后运行、维护与服务更新仍计入。'))

    page('阶段顺序与变量含义',
        p('我们先交付1亿吨普通建设材料，再在晚期逐类交付水处理模块、清水舱、原水舱和增量供电设备。随后预置初始水及运营期电梯物资，全部就绪后开始365天入住供水。水系统硬件作为1亿吨之外的增量单独计量。'),
        table(['阶段','交付对象','结束条件'],[
            ['普通建设','两路分配的通用材料','指定质量到货，停止后续派遣，结清在途并等待套件返回'],
            ['关键设备','同类模块或同类储舱','每类设备成功交付数量满足安装需求'],
            ['初始水','包装货物中的可用净水','水量保证完成，运输队列与返回套件结清'],
            ['运营物资','顶端补给货物与推进剂','指定港预置全年的有限需求及补充套件'],
            ['入住运行','生活医疗服务水','满足365天需求；停止新增派遣后结清既有在途及返程']],[1.1,2.2,3.8]),
        p('E表示电梯提升接轨道运输，R表示地面火箭直达。建设E比例、初始预置E比例和运营路线是三个不同决策。报告中“纯电梯建设”不自动表示一年供水也全走电梯；完整纯路线方案另行筛选。'),
        p('β是顶端出发湿重与载荷之比，χ是返回干结构与载荷之比，λ是推进剂整个储存期的损失情景。水台账使用W清水、Y可回收当量、P未结算补给承诺，避免把途中货物当成已可饮用的水。'))

    page('物理任务与质量接口',
        p('物理层保留圆形共面、零影响球和瞬时脉冲近似。轨道拖船停在月球100公里轨道，化学登陆器下降、卸货、上升，会合后两者返回顶端。自由释放方案与半椭圆方案在相同简化条件下比较。'),
        eq(r'A_T=\exp(\Delta v_T/(g_0 I_T)),\quad A_L=\exp(\Delta v_L/(g_0 I_L))'),
        eq(r'M_L=A_L(1+\chi_L B_L),\quad \beta=A_T(M_L+\chi_T+(\chi_T+\chi_L)(B_T-1))'),
        p('χT和χL为两者干重比，BT和BL以返程Δv按同一火箭方程定义。推导从返回干结构倒算：先保留登陆器上升推进剂，再计算下降前质量；拖船把自己及登陆器返程推进剂一并带去。不假设月面免费补充推进剂。g0与速度须使用一致单位。'),
        eq(r'g=1+(\beta-\chi-1)/(1-\lambda),\quad \chi=\chi_T+\chi_L'),
        p('g是每吨额定载荷所需新提升量；λ是推进剂整个储存期损失上限。返回干结构首次部署另计，不能每次重算，也不能给货物按推进剂比例蒸发。'),
        table(['默认受限任务接口','值'],[
            ['顶端出发湿重每吨载荷',number(M['beta_outbound_per_net_cargo'],6)+'吨'],
            ['返回干重每吨载荷',number(M['return_dry_per_net_cargo'],3)+'吨'],
            ['触地总重每吨载荷',number(M['landing_mass_per_net_cargo'],6)+'吨'],
            ['出程时间上界',str(M['outbound_ready_to_touchdown_days_integer_scenario'])+'天'],
            ['单独返程尾部上界',str(M['return_tail_upper_days'])+'天'],
            ['可拼接周转时间接口',str(M['return_cycle_days'])+'天']],[4.4,2.7]),
        p('默认自由释放在21点名义速度目录中湿重倍率最低，尚未证明全局轨道最优。三维月球轨道、有限推力、精确交会、热控和核安全没有由本近似验证。完整公式、返程分支和相位方程见proofs/physics_v9.md。'))

    page('固定能力与服务下界',
        p('故障不按独立概率相乘。我们规定任意连续P天内至多B天停止服务，允许各类故障相关。对长度n的区间，其停止日期数由滚动预算包络控制。'),
        eq(r'b_B(n)=B\lfloor n/P\rfloor+\min(B,n\bmod P)'),
        eq(r'\beta_j(t)=R_j(t-T_j)_+,\quad R_{path}=\min_j R_j,\quad T_{path}=\sum_j T_j'),
        p('βj是服务曲线，区别于质量倍率β。开放日能力c的阶段可压低为速率c(1−B/P)与延迟B/(1−B/P)的下界；代码对离散日期嵌入另预留1天。每Δ天一个整批机会的保守速率为Q(1/Δ−B/P)。串联取最小速率并相加延迟，再留整批余量。'),
        table(['路线','固定物理来源','默认故障支持'],[
            ['E','3港，各179,000吨毛提升每年','提升停止30天；派遣停止60天；每港每年货损至多1批、永久船损至多1套'],
            ['R','10基地，各250次每年、125吨每次','每基地停止60天、货损至多1枚；月面接收组停止7天'],
            ['月面接收','按完整船次预留槽位及触地卸货能力','开放日FIFO且工作保持；停港影响整个已预留服务组']],[0.5,2.6,4.0]),
        p('提升按新增货物与推进剂毛重占用能力，月面触地按载荷加登陆器等总重计，卸货按所交载荷计。这些不同口径在资源账中分别保留。接收设施规模是设计输出，不是测得的未来额定值。'))

    page('建设货损与备用船证明',
        p('每一物理来源独立保留货损预算j和永久套件损失预算h。每次失败占用一次尝试；失败的货物从成功交付中扣除，补发尝试、推进剂和制造费用一并计入。为避免取整导致工期函数局部下降，先用损失计数的仿射上界求充分工期。'),
        eq(r'S(H)=\lceil hH/P+h\rceil,\quad b_h(H)\le hH/P+h\le S(H)'),
        eq(r'L(H)=r((1-a_1)H-a_0-T_{path}-1)-4Q-Q(jH/P+j)'),
        p('a1来自备用船随工期增加而增加的首次部署负担；a0包含部署固定延迟、基本轮转船和取整余量。L(H)斜率为正时，解L(H)达到该来源承担的材料量，再把船数、部署天数、源流量和损失重新代回整数式检查。'),
        p('船队由保证周转的基本轮转套件与有限运行期备用组成。备用套件在使用前已提升到该港，首次干重只计一次；永久损失后不能再次被复用。建设结束后只把保证完好的基本船数传给下一阶段。'),
        p('派遣在该阶段截止日停止。在途批次继续结算，未派遣尾货隔离保留，下一阶段不把它当作免费水或设备。由此所有实际派遣日期均在所计货损和船损预算内，交接尾部不会漏计新的派遣。'),
        p('长期备用就绪依赖明确的维护与更新服务条件。前置存放大量备用套件不证明其能自然保存数百年；年度维护支出只是成本参数，也不能代替耐久性证据。详见proofs/construction_v9.md。'))

    page('关键设备身份与跨阶段资源',
        p('总质量达到目标不代表每一种关键设备都到了。v9把处理模块、清水舱、原水舱和供电模块分成同类货物批次，并在晚期交付。对单件质量m和载荷上限Q，每批计划装k件同类设备，k由所选包装政策决定。'),
        eq(r'1\le k\le\lfloor Q/m\rfloor,\quad N_{good}\ge\lceil n_{required}/k\rceil'),
        p('运输证明保证足够数量的完整成功批次，就保证该设备的交付件数。制造账按全部可能分配的整批设备计费，包含失败和隔离尾货；运行功率只按实际需要安装的模块数计算。载荷不足处按额定载荷上界计运输资源，不能误称空余容积具有质量。'),
        table(['资源','阶段交接的处理'],[
            ['兼容套件','逐港复用保证完好的基本船数；不足部分和本阶段备用另行购买并提升'],
            ['顶端仓库','保留全部可能未损失的旧套件、历史隔离货物、当前流量积压和运营物资'],
            ['接收服务','同阶段相加，顺序阶段取预订容量最大规模；完整船次、触地和卸货同时核对'],
            ['运营电梯物资','一年新货和推进剂在入住前存于指定港，只使用该港固定提升能力'],
            ['设施维护','按实际首次需要该设施的阶段起计暴露年数，避免把晚建资产倒计数百年维护']],[1.5,5.6]),
        p('新增供电模块采用40千瓦、6吨的设计预算，功率包含连续供电、调节及热控要求。NASA概念研究把40千瓦和低于6吨列为目标，并未验证现成产品。故障模式另加一套发电备用。物理设备清单限于载具、载荷、水模块、储舱和供电模块；外部仓储及接收设施部署仍依赖前置服务。'))

    representative=['stock_all','recycle_0.94_R_2independent_zones','recycle_0.98_R_2flights_daily','recycle_0.98_R_2independent_zones','recycle_0.98_E_every2days','recycle_0.98_ER_halfzones']
    wr=[]
    for name in representative:
        z=water_index[name]
        if z['feasible']:wr.append([water_label(name),number(z['initial_lunar_water_t'],0),str(z['processing_modules']),f"{z['fresh_tank_compartments']} / {z['raw_tank_compartments']}",str(z['operating_R_flights']),str(z['operating_E_fleet'])])
    page('供水路线与回收率分开比较',
        p(f"每种模式保留{len(water)}个供水候选；默认故障支持下{len(feasible_water)}个通过充分证书。未通过的候选连同原因保留，不能把证书不成立直接写成所有政策下物理不可行。"),
        eq(r'n_{mod}=s+\lceil\eta GP/(k_{mod}(P-R_{proc}))\rceil,\quad K=(n_{mod}-s)k_{mod}'),
        p('每个独立水区按上式选整数处理模块。kmod为模块产出能力，s是允许离线模块数，Rproc为整个处理系统停止日期预算；K已扣除离线模块，不能再次扣减。'),
        table(['供水方案','初始净水吨','处理模块','清水舱与原水舱','年R枚数上界','E套件'],wr,[2.0,1.05,.75,1.05,.85,.7]),
        p('R整批方案可由两个或四个基地共同完成一批。另有两个或四个独立人口分区，各自维护水循环、备用与单基地补给。ER方案让两个人口区分别由E和R供应，避免在没有证明时假设库存可任意共用。'),
        p('一年全预存是合法对照，不需要回收设备和运营补给，但要运输并保存全部水量。其储水设备、包装运输、晚期交付及保存条件均进入相同账本。'),
        p('表中是所需安装设备和年度运输上界。关键设备货损后的全部制造尝试另见政策成本特征，因此制造总数可能大于安装总数。'))

    page('供水库存与原水损失证明',
        p('服务用水G产生可回收流，正常回收比例为η。Y是可回收清水当量，W是清水，P_t是未结算补给承诺。此页Q为每批可用净水，区别于运输载荷；H_t为累计损失，区别于建设工期H。周期P仍为365天。'),
        eq(r'W_t+Y_t+P_t=r-H_t+QN_t'),
        p('r为初始备用清水，N为累计派遣数。H累计正常净消耗、收集损失、截止货损和隔舱事故损失。派遣根据已观察到的库存位置决定，具有因果性。共同故障、额外收集与额外处理故障分别受滚动预算限制，相关性可任意。'),
        eq(r'r\ge Q+\sup_{n\ge M}(A(n)-S(n-M))'),
        p('A是需求、联合收集损失与处理积压、货损及隔舱损失的上包络；S是关闭日期下仍能完成的派遣下界。对同一损失加积压量，分别证明两个安全上界再取最小；其周期尾部严格下降，使无限扫描可以缩成有限计算。完整集合分割证明保存在proofs/water_v9.md及所引用的库存推导。'),
        eq(r'Y\leftarrow Y-\eta z_{raw},\quad H\leftarrow H+\eta z_{raw},\quad \eta z_{raw}\le C'),
        p('原水舱损失zraw减少未来可回收当量，清水舱损失直接减少W，两者均保持台账守恒。原水的额外负跳只会减小积压上界，因此已有联合包络仍可使用。事故总预算同时约束两类舱。'),
        p('清水与原水分设储舱，各留容量备用。原水容量还覆盖当天处理前的输入峰值。以上是数量保证；净化质量、污染隔离、换舱清洗和保存期属于设备必须满足的工程条件。'))

    page('多基地并集与返程时间上界',
        p('多个基地合成一批时，任一基地关闭都可能使整批无法派遣。如果每基地每年最多关闭60天，不能仍把整批关闭预算设为60天。名义250开放日期还带来115个关闭日期。'),
        eq(r'B_{R,batch}\le115+n_{site}\,60,\quad J_{R,batch}\le n_{site}'),
        p('例如两基地整批使用235天关闭预算与2批货损预算。此并集上界保守但允许各基地错开故障；独立分区方案则各自用单基地预算。月面接收采用整组关闭支持，开放日保证所有预留槽位服务。'),
        eq(r'\alpha(n)=\lceil(n+u-l)/\Delta\rceil,\quad M=u+h_{receive}-1'),
        p('原始到港包络与FIFO接收服务给队长及处理日期上界，形成完成交付截止M。后续到港不能插队。接收预留按实际火箭枚数计算，例如每批两枚、每天四批接收槽对应八枚火箭。'),
        eq(r'F_0=\lceil(M+T_{return}+a)/\Delta\rceil,\quad F_{spare}=b_h(T_{dispatch})'),
        p(f"默认出程就绪上界为{M['outbound_ready_to_touchdown_days_integer_scenario']}天，返程尾部上界为{M['return_tail_upper_days']}天，可拼接周转为{M['return_cycle_days']}天。物流到港区间是含受控等待的服务合同：较早到达者等至规定日期才呈交接收器。两个取整上界相减未必仍是差值上界，代码直接使用单独证明的返程尾部。"),
        p('每个正常套件或永久损失的确认都须在周转期限内完成，备用在a天内激活。备用数仅保护有限派遣期和结算尾部；更长运行须重新配置补充资源。'))

    baseline_rows=[]
    for mode in ['ideal','fault']:
        for r in ['R','E','ER']:
            z=next(z for z in J['construction_summary'] if z['mode']==mode and z['route']==r)
            baseline_rows.append([modeword[mode],route(r),number(z['E_share']*100,2)+'%',number(z['delivery_upper_years'],2)])
    page('三路线固定能力基准结果',
        table(['模式','建设路线','E承担材料比例','充分交付上界 年'],baseline_rows,[1.1,2.0,1.8,2.2]),
        pic('construction_times_v9.png'),
        p('联合路线的表值取当前材料比例目录内交付上界最短者；目录额外包含两条仿射工期线的平衡比例。理想与故障模式保持相同物理来源数量和额定能力，只改变所列故障支持。'),
        p('这些数值是本服务构造保证足够交付的上界。取整、每来源整批余量、全备船前置部署及停止派遣后的隔离处理会带来保守性，未证明任意工程调度的最短工期。'),
        p('数百年量级提示：若希望几十年建成，必须另行研究实际能力提升、施工规模或任务架构。主基准不会把扩容偷偷计入现有三港能力。'))

    selected_rows=[]
    for title,r in [('中央系数预算最低',chosen),('当前入住上界最短',fastest),('中央系数最佳全预存',stock)]:
        selected_rows.append([title,number(r['habitation_upper_days']/365,1),number(r['scenarios']['central']['cost_usd']/1e12,2),water_label(r['water_id'])])
    page('完整政策的预算与工期取舍',
        pic('cost_time_v9.png'),
        table(['目录中选法','入住上界 年','情景预算 万亿美元','水策略'],selected_rows,[2.0,1.15,1.45,2.5]),
        p(f"中央系数最低预算方案使用{route(chosen['construction_route'])}建设、{prep(chosen['preposition_E_share'])}交付晚期设备和初始水、{route(chosen['operation_route'])}运营补给。这三个路线标签应一起说明。"),
        p('工期与费用预算是两个目标。前沿保留那些没有其他已存候选能同时提供更短上界和更低预算的政策。若决策者有入住期限，应在此前沿上施加期限后重新选择，不能只按预算推荐最慢路线。'),
        p('图中美元为统一常技术系数下、对所列资源上界计费的未折现预算。实际尝试和支出可能更少。设备包装比较容量装满、按需求匹配、每批单件，以及处理模块每批两件四种政策，仍未证明任意包装调度的实际最优。'))

    defs=J['cost_environment_definitions'];bench=defs['historical_benchmarks']
    page('费用参数与区间的数学含义',
        eq(r'B(x;c)=\sum_j c_j f_j(x)'),
        p('B是事前资源预算。f包含毛提升量、电能、推进剂、分配尝试上界、套件设备、容量预订及维护暴露量；这些上界不一定同时实现。R单次服务费含载具、推进剂与发射服务。365天需求结束后的既有在途结算和返程尾部仍计设施维护，不再增加供水需求或新派遣。'),
        eq(r'B_{lo}(x)=\sum_j\underline c_j f_j(x),\quad B_{hi}(x)=\sum_j\overline c_j f_j(x)'),
        p('特征非负时，对固定预算特征向量，系数盒内精确最小和最大预算由端点给出。下端点不是实际支出的下界，也不是置信下限。未来单价范围是具名情景，未由历史价格直接校准；政策须在同一组系数下比较。'),
        table(['一手历史标尺','已核对数值','用于本项目的边界'],[
            ['NASA Psyche 2020发射合同','约1.17亿美元','仅作量级参考；不是未来125吨月球运输报价'],
            ['EIA 2024美国工业电价','0.0813美元每千瓦时','历史全国零售均值，不是2050年赤道采购价'],
            ['EIA 2023美国发电碳强度','0.81磅每千瓦时','历史发电口径，用作系数情景参考'],
            ['FAA 2020 Falcon Heavy直接排放','10次发射合计11,613吨CO₂','直接发射标尺，不能等同全部未来任务排放']],[2.1,1.8,3.2]),
        p('原有电梯系统视为已建成资产；新增水设备和载具计制造，仓储及接收容量计外部服务预订费。年度维护费用依赖提供方维持就绪和更新的合同条件，不证明真实百年寿命，也未闭合更换零件运输。完整系数和出处在cost_environment_v9.py及evidence目录。'))

    eps=J['selections']['central']['epsilon_rows'];er=[]
    for z in [eps[0],eps[len(eps)//2],eps[-1]]:
        r=index[z['selected_policy_id']]
        er.append([number(z['emissions_budget_kg']/1e12,2),number(z['cost_usd']/1e12,2),number(r['construction_E_share']*100,1)+'%',number(r['habitation_upper_days']/365,1)])
    page('环境代理量与约束优化',
        eq(r'E_{proxy}=g_{grid}E_{earth}+e_RN_R+e_{prop}M_{prop}+e_LE_{lunar}'),
        p('环境部分计入地面提升电力、火箭直接发射与上游情景、E推进剂生产及月面能源上游代理量。图中低碳电网情景只改变电力排放系数，不能据此证明总体环境最优。'),
        pic('environment_v9.png'),
        eq(r'\min_{x\in\mathcal C} B(x)\quad\mathrm{s.t.}\quad E_{proxy}(x)\le\varepsilon'),
        table(['排放代理预算 万亿千克','情景费用预算 万亿美元','建设E比例','入住上界 年'],er,[2.0,1.85,1.35,1.9]),
        p('ε约束在保存的同口径候选中，选择满足排放代理预算的最低费用预算政策。目录无可行候选不证明所有架构均不可能。黑碳、氮氧化物、臭氧、核辐射、土地海洋生态及完整上游制造尚未量化，也没有被默认为零。'))

    scenario_names={'central':'中央单价情景','rocket_favoured':'火箭较便宜情景','elevator_favoured':'电梯较便宜情景','low_carbon_grid':'低碳电网情景','high_carbon_grid':'高碳电网情景'}
    sr=[]
    for scenario in ['central','rocket_favoured','elevator_favoured']:
        r=index[J['selections'][scenario]['min_cost_policy_id']]
        sr.append([scenario_names[scenario],route(r['construction_route']),water_label(r['water_id']),number(r['scenarios'][scenario]['cost_usd']/1e12,2),number(r['habitation_upper_days']/365,1)])
    de=[z for z in J['deadline_stress'] if z['deadline_years'] in [50,250,350,500,1000,1500]]
    page('敏感性与期限查询',
        table(['系数情景','建设路线','供水候选','情景预算 万亿美元','入住上界 年'],sr,[1.6,1.0,2.1,1.25,1.15]),
        p('上表每次在整个已存目录内重新选优，体现单价改变可能引起的策略切换。它与固定两政策的盈亏平衡比较不同；后者只改变某一系数，不重新优化政策。'),
        eq(r'B(x;c)-B(y;c)=\sum_j c_j(f_j(x)-f_j(y))'),
        table(['附加入住期限 年','通过证书的目录政策数'],[[str(z['deadline_years']),str(z['certified_candidates'])] for z in de],[3.55,3.55]),
        p('期限是附加查询，主基准仍以固定能力求工期。没有通过某个期限的候选，只说明本充分服务目录没有给出相应保证。若要研究扩容，应另给投资、施工和新增能力的约束。'),
        p('当前已比较两种轨道任务、理想与故障支持、建设材料比例、预置路线、回收率、分区方式和费用系数。连续参数交互、真实价格校准及动态技术变化仍超出此有限目录。'))

    S=read('sensitivity_v9.json');scount=S['counts'];cases={r['point_id']:r for r in S['cases']}
    stress_points=[('power_limit_4000','水厂功率上限4000千瓦'),
        ('power_limit_5000','水厂功率上限5000千瓦'),
        ('warehouse_limit_250000','仓储上限25万吨'),
        ('warehouse_limit_1e+06','仓储上限100万吨'),
        ('warehouse_limit_2e+06','仓储上限200万吨'),
        ('R_calendar_365','R每基地365日名义机会'),
        ('counted_faults_1.5','计数故障预算1.5倍'),
        ('propellant_loss_0.2','推进剂总期损失20%')]
    stress_rows=[]
    for key,title in stress_points:
        if key not in cases:continue
        z=cases[key]['best_by_coefficient_scenario'].get('central')
        if not z:stress_rows.append([title,'无','无目录保证','无']);continue
        stress_rows.append([title,number(z['construction_E_share']*100,1)+'%',water_label(z['water_id']),number(z['cost_USD']/1e12,3)])
    heavy=cases.get('module_mass_50',{}).get('best_by_coefficient_scenario',{}).get('central',{})
    normal=cases.get('baseline',{}).get('best_by_coefficient_scenario',{}).get('central',{})
    light=cases.get('module_mass_5',{}).get('best_by_coefficient_scenario',{}).get('central',{})
    mass_note=('50吨模块点的预算略低于20吨点，源于此有限包装规则的离散超送量及固定单位制造价。它不是“设备越重越好”的物理结论；应同时核对制造件数和运输上界。'
        if heavy and normal and heavy['cost_USD']<normal['cost_USD']-1 else
        ('5、20和50吨模块的中央系数最低预算相同，因为每批两件的配置在三个点均可用，而运输按额定整批计费。这是装载粒度下的预算平坦，不代表实际质量没有变化或连续调度中质量不重要。'
         if heavy and normal and light and abs(heavy['cost_USD']-normal['cost_USD'])<1 and abs(light['cost_USD']-normal['cost_USD'])<1 else
         '模块质量变化同时改变整数装载与额外制造件数。其预算响应要结合物理运输量、装载规则和制造单价解释，不能只看总预算。'))
    page('工程敏感性实际发现',
        p(f"新增单因子研究覆盖{scount['declared_unique_input_points']}个输入点，去重为{scount['unique_physical_catalogue_runs']}次物理目录运行，保存{scount['saved_policy_instances']}个政策实例，其中{scount['saved_integrated_feasible_policy_instances']}个满足所加资源限制。"),
        table(['改变的条件','建设E比例','中央系数获选供水','情景预算 万亿美元'],stress_rows,[2.25,1.05,2.55,1.25]),
        p('这些点统一采用较粗建设比例、E或R预置路线，以及按需求匹配和处理模块每批两件两种包装规则。主目录另比较两种包装规则与更细比例，因此两组最小值不能混称为同一个最优值。'),
        p(mass_note),
        p(f"{scount['nested_limit_checks']}项嵌套资源限制检查通过。故障因子0仅移除计数故障，仍保留抖动与推进剂损失设定，不等同第11页完整理想模式；提升能力变化是另列反事实，未替换三港主基准。"))

    def find_count(key,default_value='见核验记录'):
        def walk(x):
            if isinstance(x,dict):
                if key in x and isinstance(x[key],(int,float,str)):return x[key]
                for v in x.values():
                    z=walk(v)
                    if z is not None:return z
            return None
        z=walk(V);return default_value if z is None else z
    labels=[('independent_mass_and_velocity_records','质量与速度记录'),
        ('independent_components','供水组件'),
        ('scalar_interval_points_including_extended_tails','标量区间点'),
        ('independent_fault_and_raw_loss_paths','小故障及原水损失路径'),
        ('suffix_interval_checks','后缀区间'),
        ('independent_small_arrival_and_closure_cases','小到港及停港组合'),
        ('independent_policy_certificates','建设政策证书')]
    countlines='独立实现另核对'+ '、'.join(str(find_count(k))+label for k,label in labels if isinstance(find_count(k),int))+'。'
    page('独立核验与证据范围',
        table(['生产端检查','实际范围'],[
            ['物理质量链',str(P['checks']['mission_mass_chains'])+'条；逐段返回质量重建'],
            ['出返程ODE',str(P['checks']['outgoing_and_incoming_ODE_integrations'])+'次；核对轨道位置、能量和返回速度'],
            ['圆形交会相位',str(P['checks']['circular_interception_phase_cases'])+'组；仅对应所列简化几何'],
            ['水量逐日回放',str(W['validation']['path_count'])+'条365天路径；包括原水与清水舱损失'],
            ['联合政策目录',str(len(J['candidates']))+'个保存政策；完整阶段登记与输入可追溯'],
            ['独立检查总开关','all_implemented_checks_pass = true']],[2.0,5.1]),
        p('独立检查用另一实现核对关键不等式、质量账、队列和阶段资源。完整数量与范围以results/independent_v9.json为准，避免把不同对象或重复案例加成一个“验证次数”。'),
        p(countlines),
        p('有限小日历穷举与代表路径不能穷尽所有未来事故。模型保证来自明确支持与证明；程序检查用于寻找实现和接口错误。故障路径是生成情景，不能当成NASA故障实测，也没有估计真实缺水概率。'),
        p('解压复算和文档生成检查在交付前单独完成，其结果记录于复现包。运行一致性不能替代真实载具、月面水厂、储存、水质及核安全认证。'))

    page('一手资料与证明阅读位置',
        links([
            ('官方MCM 2026 B题面','https://www.comap.com/contests/mcm-icm','本包evidence/2026_MCM_Problem_B.pdf第1至2页为任务和尺度；网页仅为主办方入口。'),
            ('JPL天体参数','https://ssd.jpl.nasa.gov/astro_par.html','地月引力参数与时间单位。物理常数不证明未来运输硬件性能。'),
            ('NASA理想火箭方程','https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/ideal-rocket-equation/','动量与质量比公式；本项目另推导携带返程推进剂的分阶段质量链。'),
            ('NASA月面裂变供电概念目标','https://www.nasa.gov/centers-and-facilities/glenn/nasas-fission-surface-power-project-energizes-lunar-exploration/','2024年文中40千瓦、低于6吨及十年设计目标。当前6吨是预算取值，不能当成已验证产品质量。'),
            ('Peet 2020空间电梯释放研究','https://arxiv.org/abs/2008.05244','自由释放的架构背景及平面、方向和交会限制；本项目月球双曲线数值为自行计算。'),
            ('Le Boudec与Thiran网络演算','https://leboudec.github.io/netcal/latex/netCalBook.pdf','PDF40页定理1.4.1与46页定理1.4.6，积压界和串联服务。'),
            ('NASA Psyche发射合同','https://www.nasa.gov/news-release/nasa-awards-launch-services-contract-for-the-psyche-mission/','2020年公告正文前两段，约1.17亿美元合同范围；不直接迁移为未来月球运价。'),
            ('EIA电价与发电排放','https://www.eia.gov/electricity/annual/table.php?t=epa_01_01.html','2024工业均价见Table1.1；排放FAQ链接与单位转换见成本环境来源索引。'),
            ('FAA Falcon项目环境评估','https://www.faa.gov/sites/faa.gov/files/space/environmental/nepa_docs/SpaceX_Falcon_Program_Final_EA_and_FONSI.pdf','PDF90页、印刷71页Table4-4直接发射CO₂；不混用不同系统边界的其他表。')]),
        p('详细来源、实际阅读位置、可支持与不可支持的主张均保存在evidence的来源索引中。新增数学推导与文献提供的工具分开说明，避免把项目情景写成文献实测结论。'))

    page('建模与编程交接及剩余边界',
        table(['文件或目录','用途'],[
            ['proofs/physics_v9.md','学习任务几何、质量链、出返程相位和独立时间上界'],
            ['proofs/construction_v9.md','学习固定能力、货损补发、备用部署和充分工期证明'],
            ['proofs/water_v9.md','学习分区目录、库存保证、原水损失、接收与有限船队'],
            ['proofs/joint_v9.md','核对关键设备身份、阶段复用、隔离尾货和费用特征'],
            ['proofs/cost_environment_v9.md','核对系数盒区间、政策比较、前沿与ε约束'],
            ['results/policy_summary_v9.csv','查看各政策的路线、供水方案、预算与时间摘要'],
            ['results/sensitivity_v9.csv','查看压力点及重新选优结果；阶段细节按政策ID追溯']],[2.8,4.3]),
        p('编程手在解压包根目录按README安装依赖，执行python run_v9.py；仅复核已有结果用python verify_v9.py。修改服务时限、能力、故障预算或单价后，须重新生成结果与报告，核对单位、整数批次和阶段接口。'),
        p('数学主线可以向老师这样说明：先以物理质量链确定每吨货需要多少提升量，再用故障支持推服务下界和交付条件，按整数批次保证关键设备及水量，最后在同一资源账上比较费用、工期和环境代理量。'),
        p('前置服务尚有实体缺口：2050年前顶端仓储、月面机器人接收设施须可用，提供方部署的质量与时间未进入物理账。长期备用和基础设施的维护就绪合同也没有真实百年寿命或更新零件物流验证。其余待闭合项是三维有限推力任务、真实载具与核安全、水质净化隔离、未来单价和完整环境影响。'),
        p('截至本轮所列检查，未发现仍未解决的模型内阻断问题；这句话的范围是本次声明的任务族、政策目录和服务支持。后续工程数据或新反例仍可能要求修改假设与结论。'))

    page('给月球殖民地管理机构的建议信',
        p('致月球殖民地管理机构：'),
        p('我们建议先确认可接受的建成时间与可落实的服务能力，再确定建设运输组合。本模型固定三港额定提升能力及所选火箭基地的名义日历，将交付时间作为结果。即使联合使用两种运输方式，当前参数下的充分工期仍为数百年量级。若机构目标是几十年建成，应另行论证扩容、施工规模与任务架构，并核算新增能力的投资和部署，而不是把扩容隐含进基准。'),
        p('在工程能力得到确认前，应保留电梯接驳和地面火箭两条路线。我们建议在同一口径的保守预算、工期保证和环境代理量前沿上进行选择。中央单价情景下预算最低的长期政策，不应仅因预算较低而成为实际工程推荐；未来运输、维护和制造价格仍需采购与工程证据。'),
        p('一年生活医疗供水可优先推进高回收率系统的验证，同时保留足够初始清水、独立原水容量、处理冗余和补给能力。98%正常回收是本目录的重要候选，其成立仍要求模块产能、连续供电、净化质量、隔舱隔离和发运时限得到验证。运营补水应同时比较火箭、电梯及分区组合，避免把回收率与单一路线绑定。'),
        p('机构还应先确认顶端仓储和月面机器人接收服务在首批建设货物到达前可用，并补齐服务方设施部署及长期维护更新的物资流。本轮对这些服务核算容量与费用，尚未给出从零建设它们的完整物流方案。'),
        p('环境决策应同时核对地面电力、推进剂上游生产及火箭排放。当前模型只量化所列运行排放代理项；黑碳、臭氧、核安全和生态影响需要专业评估后才能形成完整环境结论。建议先完成这些证据核查，再据明确的时间目标与预算选择实施方案。'),
        p('建模小组\n2026年10月28日'))
    return pages,equations


def equation_parts(equations):
    md=AS/'equations_v9.md'
    # Avoid renderer-specific stretchy-delimiter pairing issues while keeping
    # OMML searchable and editable. Braces used as mathematical sets stay TeX.
    clean=[re.sub(r'_\{([A-Za-z]{2,})\}',lambda m:'_{\\mathrm{'+m.group(1)+'}}',s)
        for s in equations]
    md.write_text('\n\n'.join('$$\n'+s+'\n$$' for s in clean),encoding='utf-8')
    target=AS/'equations_v9.docx'
    p=subprocess.run(['pandoc',str(md),'-f','markdown+tex_math_dollars','-t','docx','-o',str(target)],capture_output=True,text=True)
    if p.returncode or 'Could not convert' in p.stderr:raise RuntimeError(p.stderr)
    d=Document(target);parts=[x for x in d.element.body if x.find('.//'+qn('m:oMath')) is not None]
    if len(parts)!=len(equations):raise RuntimeError('Native equation count mismatch')
    return dict(zip(equations,parts))


def hyperlink(par,label,url):
    rid=par.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),rid)
    run=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'245E7A');pr.append(c)
    run.append(pr);t=OxmlElement('w:t');t.text=label;run.append(t);h.append(run);par._p.append(h)


def add_table(doc,heads,rows,widths):
    widths=widths or [7.1/len(heads)]*len(heads)
    t=doc.add_table(rows=1,cols=len(heads));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for col,w in zip(t.columns,widths):col.width=Inches(w)
    for i,s in enumerate(heads):t.rows[0].cells[i].text=str(s)
    header=t.rows[0]._tr.get_or_add_trPr();header.append(OxmlElement('w:tblHeader'))
    for row in rows:
        cells=t.add_row().cells
        for i,s in enumerate(row):cells[i].text=str(s)
    borders=OxmlElement('w:tblBorders')
    for name in ['top','left','bottom','right','insideH','insideV']:
        b=OxmlElement('w:'+name);b.set(qn('w:val'),'single');b.set(qn('w:sz'),'4');b.set(qn('w:color'),'D9D9D9');borders.append(b)
    t._tbl.tblPr.append(borders)
    for ri,row in enumerate(t.rows):
        row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        for ci,cell in enumerate(row.cells):
            cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
            for side,n in [('top',70),('bottom',75),('left',90),('right',90)]:
                el=OxmlElement('w:'+side);el.set(qn('w:w'),str(n));el.set(qn('w:type'),'dxa');mar.append(el)
            tcpr.append(mar)
            if ri==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DDE9EF');tcpr.append(shade)
            for pp in cell.paragraphs:
                pp.paragraph_format.space_after=Pt(0);pp.paragraph_format.line_spacing=1.02
                if len(heads)>=4 and ci>0:pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for rr in pp.runs:rr.font.size=Pt(8.9 if len(heads)>=5 else 9.2);rr.bold=ri==0
    pp=doc.add_paragraph();pp.paragraph_format.space_after=Pt(1);pp.paragraph_format.space_before=Pt(0)


def main():
    AS.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
    J,P,W,V,index,default=data();charts(J,index,default)
    pages,equations=blocks(J,P,W,V,index,default);ep=equation_parts(equations)
    d=Document();sec=d.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.59);sec.left_margin=sec.right_margin=Inches(.68)
    sec.footer_distance=Inches(.25)
    for name in ['Normal','Title','Heading 1','Heading 2']:
        st=d.styles[name];st.font.name='Noto Sans CJK SC';st.font.color.rgb=RGBColor(0,0,0)
        st._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Noto Sans CJK SC')
    normal=d.styles['Normal'];normal.font.size=Pt(10)
    normal.paragraph_format.line_spacing=1.10;normal.paragraph_format.space_after=Pt(6)
    d.styles['Title'].font.size=Pt(22);d.styles['Title'].paragraph_format.space_after=Pt(10)
    d.styles['Heading 1'].font.size=Pt(17);d.styles['Heading 1'].paragraph_format.space_after=Pt(9)
    for b in list(d.styles.element.xpath('.//w:pBdr')):b.getparent().remove(b)
    mp=d.settings.element.find(qn('m:mathPr'))
    if mp is None:mp=OxmlElement('m:mathPr');d.settings.element.append(mp)
    font=mp.find(qn('m:mathFont'))
    if font is None:font=OxmlElement('m:mathFont');mp.append(font)
    font.set(qn('m:val'),'Latin Modern Math')
    d.core_properties.title='MCM B v9 建模修订与独立验证说明';d.core_properties.author='MCM建模小组'
    foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    rr=foot.add_run('MCM B v9  ');rr.font.size=Pt(8)
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
    for n,(title,rows) in enumerate(pages,1):
        if n>1:d.add_page_break()
        if n==1:
            d.add_paragraph('MCM B v9 建模修订与独立验证说明','Title')
            pp=d.add_paragraph('2026年10月28日  月球建设运输与一年供水  建模和编程交接')
            pp.paragraph_format.space_after=Pt(11)
        d.add_paragraph(str(n)+' '+title,'Heading 1')
        for kind,value in rows:
            if kind=='p':d.add_paragraph(value)
            elif kind=='eq':
                el=deepcopy(ep[value]);d.element.body.insert(len(d.element.body)-1,el)
            elif kind=='pic':d.add_picture(str(AS/value),width=Inches(7.1))
            elif kind=='table':add_table(d,*value)
            elif kind=='links':
                for title,url,note in value:
                    pp=d.add_paragraph();pp.paragraph_format.space_after=Pt(2);hyperlink(pp,title,url)
                    pp=d.add_paragraph(note);pp.paragraph_format.space_after=Pt(8)
                    for run in pp.runs:run.font.size=Pt(9.3)
    output=OUT/'MCM_B_v9_建模修订与独立验证说明.docx';d.save(output)
    print(json.dumps(dict(path=str(output),designed_pages=len(pages),native_equations=len(equations)),ensure_ascii=False))


if __name__=='__main__':main()
