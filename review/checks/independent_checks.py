"""Independent cross-artifact arithmetic checks for the frozen v9 first draft.

Reads JSON and extracted DOCX tables. Does not import project model modules or
write original outputs. JSON result is a bounded audit record, not a solver proof.
"""
from pathlib import Path
import argparse
import json
import math

parser=argparse.ArgumentParser()
parser.add_argument('--results',type=Path,required=True)
parser.add_argument('--paper-extract',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()

joint=json.loads((args.results/'joint_v9.json').read_text())
water=json.loads((args.results/'water_v9.json').read_text())
paper=json.loads(args.paper_extract.read_text())
checks=[]
def check(name,actual,expected,atol=1e-8):
    passed=math.isclose(float(actual),float(expected),abs_tol=atol,rel_tol=0)
    checks.append({'name':name,'actual':actual,'expected':expected,'absolute_difference':abs(float(actual)-float(expected)),'tolerance':atol,'pass':passed})

# Independently recompute the absolute physical demand and a simple capacity bound.
G=962*1.2
check('water_gross_t_day',G,water['inputs']['gross_service_t_day'])
check('water_gross_t_year',G*365,421356)
check('water_94pct_net_t_year',G*(1-.94)*365,25281.36)
check('water_98pct_net_t_year',G*(1-.98)*365,8427.12)
fixed=joint['fixed_capacity']
gross_year=fixed['harbours']*fixed['lift_gross_t_year_each']+fixed['selected_R_sites']*fixed['R_flights_year_each']*fixed['R_payload_t']
check('nominal_gross_capacity_t_year',gross_year,849500)
check('50_year_max_t',50*gross_year,42475000)
checks.append({'name':'50_year_cannot_deliver_100Mt_even_ignoring_overheads','actual':50*gross_year,'expected':'<100000000','pass':50*gross_year<100000000})

# Independently select finite-catalogue extrema from saved candidate records.
mission=joint['default_mission_key']
candidates=[p for p in joint['candidates'] if p['mode']=='fault' and p['mission_key']==mission]
min_budget=min(candidates,key=lambda p:p['scenarios']['central']['cost_usd'])
shortest=min(candidates,key=lambda p:p['habitation_upper_days'])
table=paper['tables'][6]['rows']
check('paper_min_budget_USD_trillion',min_budget['scenarios']['central']['cost_usd']/1e12,float(table[1][4]),.0005)
check('paper_min_budget_habitation_years',min_budget['habitation_upper_days']/365,float(table[1][5].replace(',','')),.005)
check('paper_shortest_budget_USD_trillion',shortest['scenarios']['central']['cost_usd']/1e12,float(table[2][4]),.0005)
check('paper_shortest_habitation_years',shortest['habitation_upper_days']/365,float(table[2][5].replace(',','')),.005)

# Compare paper's six route-category delivery bounds to the result object.
summary={(p['mode'],p['route']):p for p in joint['construction_summary']}
for i,route in enumerate(['R','E','ER'],1):
    row=paper['tables'][3]['rows'][i]
    check(f'paper_route_{route}_ideal_years',summary['ideal',route]['delivery_upper_years'],float(row[1]),.005)
    check(f'paper_route_{route}_fault_years',summary['fault',route]['delivery_upper_years'],float(row[2]),.005)

# Stock-all water is a transparent scalar identity; all policies still need
# the more elaborate service-curve and event-support audit separately.
stock=next(p for p in water['fault'] if p['id']=='stock_all')
check('stock_all_initial_t',stock['initial_lunar_water_t'],G*365+1000,.01)
check('paper_stock_all_initial_t',float(paper['tables'][5]['rows'][1][1].replace(',','')),stock['initial_lunar_water_t'],.01)

record={'basis':'frozen v9 result JSON and read-only DOCX table extraction','scope':'Independent arithmetic/cross-artifact checks; not proof of mission physics, service guarantees, global optimality, or course compliance','fault_default_candidate_count':len(candidates),'checks':checks,'pass_count':sum(x['pass'] for x in checks),'fail_count':sum(not x['pass'] for x in checks)}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':record['pass_count'],'fail':record['fail_count'],'candidate_count':len(candidates)},ensure_ascii=False))
raise SystemExit(0 if record['fail_count']==0 else 1)
