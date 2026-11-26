"""Finite, explicitly declared fixed-capacity lunar construction/water policies.

All route combinations are admitted.  Time is a certified sufficient output,
not a fixed50-year exclusion.  Separate homogeneous equipment campaigns make
critical equipment identities checkable after cargo losses.  No v8 winner is
carried into this catalogue as an assumption.
"""
from dataclasses import asdict, replace
from functools import lru_cache
from pathlib import Path
from copy import deepcopy
import csv, hashlib, json, math

from physics_v9 import chosen_mission, mission_catalog
from construction_v9 import ConstructionInputs, ideal_inputs, plan_construction
from water_v9 import WaterInputs, build_water_catalogue
from cost_environment_v9 import (evaluate_features, get_scenario_defs,
    compare_fixed_plans, pareto_frontier, epsilon_cost_minimum)
from registry_v9 import save_phase_registry

ROOT=Path(__file__).resolve().parent
P=365
GENERIC_CONSTRUCTION_T=100_000_000.
POWER_MODULE_KW=40.
POWER_MODULE_DRY_T=6.  #NASA40kW/<6t concept requirement used as a conservative named unit, not verified performance
WAREHOUSE_UNIT_T=50000.
MISSIONS={}
REGISTRY={}
ACTIVE_CONSTRUCTION_INPUTS=ConstructionInputs()


def configure_inputs(inputs=None):
    """Select an explicit construction scenario before a serial study."""
    global ACTIVE_CONSTRUCTION_INPUTS
    ACTIVE_CONSTRUCTION_INPUTS=inputs or ConstructionInputs()
    transport.cache_clear()


def mission_key(m):
    return hashlib.sha256(json.dumps(m,sort_keys=True).encode()).hexdigest()[:16]


def register_mission(m):
    key=mission_key(m);MISSIONS[key]=m;return key


@lru_cache(maxsize=None)
def transport(route, target_t, available, mode, mkey, sources):
    x=ACTIVE_CONSTRUCTION_INPUTS
    if mode=='ideal':x=ideal_inputs(x)
    if route=='E':x=replace(x,harbours=sources)
    else:x=replace(x,rocket_sites=sources)
    z=plan_construction(1. if route=='E' else 0.,x,MISSIONS[mkey],
        target_t=target_t,available_E_hulls_per_harbour=available)
    if not z['feasible']:raise RuntimeError('A fixed-source transport campaign is not certified')
    return z


def new_state():
    return dict(day=0., available=[0,0,0], ever_hulls=[0,0,0],
        quarantine=[0.,0.,0.], warehouse=[0.,0.,0.],
        harbour_first_use=[None]*3, site_first_use=[None]*10,
        hull_installs=[], warehouse_installs=[], terminal_installs=[],
        terminal_modules=0, phase_ids=[], E_new_lift_t=0., E_propellant_t=0.,
        E_flights=0, R_launches=0, equipment_manufactured={},
        E_hulls_initial=0, cargo_loss_upper_t=0., hull_loss_upper=0,
        ground_quarantine_t=0.)


def _warehouse(state, hub, requirement, now):
    required=math.ceil(max(0.,requirement)/WAREHOUSE_UNIT_T-1e-12)*WAREHOUSE_UNIT_T
    if required>state['warehouse'][hub]:
        state['warehouse_installs'].append([required-state['warehouse'][hub],now])
        state['warehouse'][hub]=required


def _terminal(state, slots, touchdown, unload, now):
    modules=max(math.ceil(slots/4),math.ceil(touchdown/(1e6/P)),math.ceil(unload/(1e6/P)))
    if modules>state['terminal_modules']:
        state['terminal_installs'].append([4*(modules-state['terminal_modules']),now])
        state['terminal_modules']=modules


def _record_phase(state, detail):
    signature=json.dumps(detail,sort_keys=True,separators=(',',':'))
    pid=hashlib.sha256(signature.encode()).hexdigest()[:20]
    REGISTRY[pid]=detail;state['phase_ids'].append(pid)


def apply_campaign(state, label, E_targets, R_target, mode, mkey,
                   item_kind=None,item_unit_t=None,item_required=None,
                   packing_E=None,packing_R=None):
    """Parallel three physical E sources and a selected ten-source R campaign.

    A hardware target is rated payload-equivalent, not a claim that empty
    packing space has physical mass. Every allocated full job has the same
    integer number of the named item. Thus enough successful full jobs proves
    item counts, as well as an upper transport mass/cost budget.
    """
    now=state['day'];m=MISSIONS[mkey];dry=m['return_dry_per_net_cargo']*500.
    entries=[];slots=touch=unload=0.;duration=0.;made=0
    for i,target in enumerate(E_targets):
        if target<=1e-9:continue
        old_avail=state['available'][i];old_ever=state['ever_hulls'][i]
        z=transport('E',float(target),old_avail,mode,mkey,1);r=z['routes']['E']
        duration=max(duration,z['ready_for_water_days'])
        if state['harbour_first_use'][i] is None:state['harbour_first_use'][i]=now
        nnew=r['hulls_installed'];state['ever_hulls'][i]+=nnew
        state['available'][i]=r['base_hulls_per_harbour_after_handoff']
        state['hull_installs'].append([nnew,now]);state['E_hulls_initial']+=nnew
        stream=r['warehouse_required_t']-r['hulls_present_after_deployment']*dry
        quarantine=r['quarantine_apex_gross_t_upper']
        # Retain ALL previously purchased hulls for no-loss storage histories;
        # only the guaranteed intact base receives a next-phase reuse credit.
        need=(state['ever_hulls'][i]*dry+state['quarantine'][i]+max(stream,quarantine))
        _warehouse(state,i,need,now)
        state['quarantine'][i]+=quarantine
        state['E_new_lift_t']+=r['new_lift_mass_t']
        state['E_propellant_t']+=r['new_lift_mass_t']-r['initial_hull_mass_t']-r['full_payload_t']
        state['E_flights']+=r['attempts_total']
        state['cargo_loss_upper_t']+=r['cargo_lost_t_upper']
        state['hull_loss_upper']+=r['hull_losses_total_upper']
        slots+=r['terminal_slots_reserved'];touch+=r['terminal_touchdown_t_open_day'];unload+=r['terminal_unload_t_open_day']
        perjob=(packing_E[i] if packing_E is not None else math.floor(500./item_unit_t+1e-12)) if item_unit_t else None
        if item_unit_t and not (1<=perjob<=math.floor(500./item_unit_t+1e-12)):raise AssertionError('Invalid E equipment manifest')
        guaranteed_items=math.ceil(r['guarantee_t']/500.-1e-9)*perjob if perjob else None
        if item_unit_t:made+=r['attempts_total']*perjob
        entries.append(dict(route='E',hub=i,transport=z,available_before=old_avail,
            ever_hulls_before=old_ever,warehouse_required_with_history_t=need,
            item_units_per_full_job=perjob,guaranteed_item_units=guaranteed_items))
    if R_target>1e-9:
        z=transport('R',float(R_target),0,mode,mkey,10);r=z['routes']['R']
        duration=max(duration,z['ready_for_water_days'])
        for i in range(10):
            if state['site_first_use'][i] is None:state['site_first_use'][i]=now
        state['R_launches']+=r['attempts_total'];state['ground_quarantine_t']+=r['quarantine_ground_payload_t_upper']
        state['cargo_loss_upper_t']+=r['cargo_lost_t_upper']
        slots+=r['terminal_slots_reserved'];touch+=r['terminal_touchdown_t_open_day'];unload+=r['terminal_unload_t_open_day']
        perjob=(packing_R if packing_R is not None else math.floor(125./item_unit_t+1e-12)) if item_unit_t else None
        if item_unit_t and not (1<=perjob<=math.floor(125./item_unit_t+1e-12)):raise AssertionError('Invalid R equipment manifest')
        guaranteed_items=math.ceil(r['guarantee_t']/125.-1e-9)*perjob if perjob else None
        if item_unit_t:made+=r['attempts_total']*perjob
        entries.append(dict(route='R',transport=z,item_units_per_full_job=perjob,
            guaranteed_item_units=guaranteed_items))
    _terminal(state,slots,touch,unload,now)
    if item_kind:
        delivered=sum(e['guaranteed_item_units'] for e in entries)
        if delivered<item_required:raise AssertionError('Critical equipment identity guarantee failed')
        state['equipment_manufactured'][item_kind]=state['equipment_manufactured'].get(item_kind,0)+made
    detail=dict(kind='transport',label=label,mode=mode,mission_key=mkey,
        start_day=now,duration_upper_days=duration,E_targets_t=list(E_targets),R_target_t=R_target,
        entries=entries,item_kind=item_kind,item_unit_t=item_unit_t,item_required=item_required,
        item_manufactured_upper=made if item_kind else None,
        terminal_slots=slots,terminal_touchdown_t_open_day=touch,terminal_unload_t_open_day=unload,
        support='Each campaign inherits the same rolling budgets on any translated interval. Summing separate interval envelopes is conservative. Dispatches cease before handoff; tail inventory is not reused as water.')
    _record_phase(state,detail);state['day']+=duration
    return detail


def ship_items(state, kind, quantity, unit_mass, share, mode, mkey,packing_policy='matched'):
    if quantity<=0:return
    if unit_mass<=0 or unit_mass>125:raise ValueError('Item must fit the declared smallest full-flight capacity')
    nE=math.ceil(quantity*share-1e-12);nR=quantity-nE
    units=[nE//3+int(i<nE%3) for i in range(3)]
    capE=math.floor(500/unit_mass+1e-12);capR=math.floor(125/unit_mass+1e-12)
    if packing_policy=='capacity_fill':bsE=[capE]*3;bsR=capR
    elif packing_policy in ['matched','module_two']:
        bsE=[min(capE,max(1,n)) for n in units];bsR=min(capR,max(1,math.ceil(nR/10)))
        if packing_policy=='module_two' and kind=='water_modules':
            if min(capE,capR)<2:raise ValueError('Two-module packing exceeds a full flight')
            bsE=[2]*3;bsR=2
    elif packing_policy=='single_item':bsE=[1]*3;bsR=1
    else:raise ValueError('Unknown homogeneous equipment packing policy')
    Et=[math.ceil(n/b)*500. if n else 0. for n,b in zip(units,bsE)]
    Rt=math.ceil(nR/bsR)*125. if nR else 0.
    apply_campaign(state,'late_'+kind,Et,Rt,mode,mkey,
                   item_kind=kind,item_unit_t=unit_mass,item_required=quantity,
                   packing_E=bsE,packing_R=bsR)


def stage_operating_E(state, water, mode, mkey):
    m=MISSIONS[mkey];now=state['day'];dry=m['return_dry_per_net_cargo']*500.
    details=[];duration=0.
    # The catalogue currently has at most one E zone. Multiple E zones would
    # require distinct dispatch/receiver reservations rather than silent pooling.
    comps=[c for c in water['components'] if c['route']=='E']
    if len(comps)>1:raise ValueError('Multiple E zones need an explicit hub assignment')
    for c in comps:
        hub=0;base=c['operating_E_base_fleet'];spare=c['operating_E_spare_hulls']
        deficit=max(0,base-state['available'][hub]);new=deficit+spare
        old_available=state['available'][hub]
        old=state['ever_hulls'][hub];state['ever_hulls'][hub]+=new
        state['available'][hub]=max(old_available,base)
        state['E_hulls_initial']+=new;state['hull_installs'].append([new,now])
        if state['harbour_first_use'][hub] is None:state['harbour_first_use'][hub]=now
        mass=c['apex_stock_gross_t']+new*dry
        x=ACTIVE_CONSTRUCTION_INPUTS;x=ideal_inputs(x) if mode=='ideal' else x
        alpha=1-x.lift_closed_days/P;rate=x.lift_t_year_per_harbour/P*alpha
        days=math.ceil(x.lift_closed_days/alpha+1+x.climber_transit_days+mass/rate) if mass>0 else 0
        need=state['ever_hulls'][hub]*dry+state['quarantine'][hub]+c['apex_stock_gross_t']
        _warehouse(state,hub,need,now)
        state['E_new_lift_t']+=mass
        state['E_propellant_t']+=c['apex_stock_gross_t']-c['annual_E_packed_cargo_t']
        state['E_flights']+=c['annual_E_departures']
        duration=max(duration,days)
        details.append(dict(hub=hub,available_intact_before=old_available,
            ever_hulls_before=old,required_base=base,operation_spares=spare,new_hulls=new,
            dry_mass_per_hull_t=dry,staged_new_mass_t=c['apex_stock_gross_t'],
            total_new_lift_t=mass,warehouse_requirement_t=need,
            fixed_gross_lift_t_day=rate,lift_and_climber_latency_days=x.lift_closed_days/alpha+1+x.climber_transit_days,
            duration_upper_days=days))
    if details:
        _record_phase(state,dict(kind='apex_water_staging',start_day=now,duration_upper_days=duration,
            mission_key=mkey,mode=mode,components=details))
        state['day']+=duration


def operation_tail_days(water):
    return max((c['fleet_certificate']['rotation_hold_days'] if c['route']=='E'
                else c['receiver']['Lmax'] for c in water['components']),default=0)


def feature_vector(state, water, mkey, operation=True):
    tail=operation_tail_days(water) if operation else 0
    end=state['day']+(water['water_horizon_days']+tail if operation else 0)
    activeR=int(water.get('operating_R_sites_required',0)) if operation else 0
    if activeR>10:raise AssertionError('More than ten R sites allocated')
    for i in range(activeR):
        if state['site_first_use'][i] is None:state['site_first_use'][i]=state['day']
    if operation:
        _terminal(state,water['receiver_actual_flight_slots'],water['receiver_touchdown_t_per_open_day'],
            water['receiver_unload_t_per_open_day'],state['day'])
    made=state['equipment_manufactured'];hours=(water['water_horizon_days']+tail)*24 if operation else 0
    f=dict(E_new_lift_t=state['E_new_lift_t'],E_energy_kWh=state['E_new_lift_t']*1000*ACTIVE_CONSTRUCTION_INPUTS.lift_kWh_kg,
        E_propellant_t=max(0.,state['E_propellant_t']),
        R_launches=state['R_launches']+(water['operating_R_flights'] if operation else 0),
        E_hulls_initial=state['E_hulls_initial'],E_flights=state['E_flights'],
        water_modules=made.get('water_modules',0),
        tanks=made.get('fresh_tanks',0)+made.get('raw_tanks',0),
        lunar_energy_kWh=water['plant_power_kW']*hours if operation else 0.,
        lunar_power_capacity_kW=made.get('power_modules',0)*POWER_MODULE_KW,
        warehouse_capacity_t=sum(state['warehouse']),
        lunar_receiving_slots=4*state['terminal_modules'],
        active_harbours=sum(t is not None for t in state['harbour_first_use']),
        active_R_sites=sum(t is not None for t in state['site_first_use']),infrastructure_years=end/P,
        harbour_service_years=sum((end-t)/P for t in state['harbour_first_use'] if t is not None),
        R_site_service_years=sum((end-t)/P for t in state['site_first_use'] if t is not None),
        hull_service_years=sum(n*(end-t)/P for n,t in state['hull_installs']),
        warehouse_t_years=sum(n*(end-t)/P for n,t in state['warehouse_installs']),
        receiving_slot_years=sum(n*(end-t)/P for n,t in state['terminal_installs']))
    if evaluate_features(f)['missing_features']:raise AssertionError('An economic feature dimension is missing')
    return f


def build_policy(share, water, prep_share, mode, mkey, *, construction_only=False,packing_policy='matched'):
    state=new_state();Et=[GENERIC_CONSTRUCTION_T*share/3]*3;Rt=GENERIC_CONSTRUCTION_T*(1-share)
    first=apply_campaign(state,'generic_100Mt_construction',Et,Rt,mode,mkey)
    delivery=max((e['transport']['construction_completion_upper_days'] for e in first['entries']),default=0.)
    generic_ready=state['day']
    if not construction_only:
        # Equipment is additional to the generic100Mt and arrives close to use.
        # Homogeneous item campaigns, not a mass-only aggregate, guarantee BOM.
        wx=water['input_scenarios']
        ship_items(state,'water_modules',water['processing_modules'],wx['module_dry_mass_t'],prep_share,mode,mkey,packing_policy)
        ship_items(state,'fresh_tanks',water['fresh_tank_compartments'],wx['tank_dry_mass_t'],prep_share,mode,mkey,packing_policy)
        ship_items(state,'raw_tanks',water['raw_tank_compartments'],wx['tank_dry_mass_t'],prep_share,mode,mkey,packing_policy)
        power_units=(math.ceil(water['plant_power_kW']/POWER_MODULE_KW)
                     +(1 if mode=='fault' else 0)) if water['plant_power_kW']>0 else 0
        ship_items(state,'power_modules',power_units,POWER_MODULE_DRY_T,prep_share,mode,mkey,packing_policy)
        packed=water['initial_lunar_packed_t']
        apply_campaign(state,'initial_usable_water',[packed*prep_share/3]*3,packed*(1-prep_share),mode,mkey)
        stage_operating_E(state,water,mode,mkey)
    f=feature_vector(state,water,mkey,not construction_only)
    scenarios={}
    for scenario in get_scenario_defs()['scenarios']:
        ev=evaluate_features(f,scenario)
        scenarios[scenario]={k:ev[k] for k in ['cost_usd','cost_interval_usd','CO2proxy_kg','emissions_proxy_interval_kg']}
    rid=hashlib.sha256(json.dumps([mode,mkey,share,water['id'],prep_share,construction_only,packing_policy]).encode()).hexdigest()[:18]
    return dict(id=rid,mode=mode,mission_key=mkey,construction_E_share=share,
        construction_route='R' if share==0 else ('E' if share==1 else 'ER'),
        preposition_E_share=prep_share,equipment_packing_policy=packing_policy,
        water_id=water['id'],operation_route=water['operation_route'],eta=water['eta'],
        generic_construction_delivery_upper_days=delivery,generic_construction_ready_days=generic_ready,
        habitation_upper_days=state['day'] if not construction_only else None,
        additional_preposition_upper_days=state['day']-generic_ready,
        water_service_end_upper_days=state['day']+water['water_horizon_days'] if not construction_only else None,
        operation_settlement_tail_upper_days=operation_tail_days(water) if not construction_only else 0,
        policy_end_upper_days=state['day']+(0 if construction_only else water['water_horizon_days']+operation_tail_days(water)),
        phase_ids=state['phase_ids'],features=f,scenarios=scenarios,
        installed_water_modules=water['processing_modules'] if not construction_only else 0,
        installed_fresh_tanks=water['fresh_tank_compartments'] if not construction_only else 0,
        installed_raw_tanks=water['raw_tank_compartments'] if not construction_only else 0,
        required_water_plant_power_kW=water['plant_power_kW'] if not construction_only else 0,
        warehouse_capacity_per_harbour_t=state['warehouse'],
        guaranteed_intact_E_base_at_operation=state['available'],E_hulls_ever_deployed=state['ever_hulls'],
        quarantined_apex_mass_per_harbour_t=state['quarantine'],
        quarantined_R_ground_payload_t=state['ground_quarantine_t'],
        purchased_equipment_upper=state['equipment_manufactured'],
        construction_cargo_loss_upper_t=state['cargo_loss_upper_t'],
        construction_hull_loss_upper=state['hull_loss_upper'],
        comparison_scope='Finite policy catalogue, sufficient service upper times and named constant-technology coefficient scenarios; no unrestricted optimum or real future price claim.')


def share_catalogue(mode,mkey):
    x=ACTIVE_CONSTRUCTION_INPUTS;x=ideal_inputs(x) if mode=='ideal' else x
    ep=plan_construction(1,x,MISSIONS[mkey])['routes']['E']
    rp=plan_construction(0,x,MISSIONS[mkey])['routes']['R']
    ae=GENERIC_CONSTRUCTION_T/(3*ep['affine_net_rate_t_day_per_source']);ar=GENERIC_CONSTRUCTION_T/(10*rp['affine_net_rate_t_day_per_source'])
    be=ep['affine_intercept_t_per_source']/ep['affine_net_rate_t_day_per_source'];br=rp['affine_intercept_t_per_source']/rp['affine_net_rate_t_day_per_source']
    balanced=max(0.,min(1.,(ar+br-be)/(ae+ar)))
    return sorted(set([k/20 for k in range(21)]+[round(balanced,8)]))


def select_and_frontiers(candidates):
    out={};defaults=[r for r in candidates if r['mode']=='fault' and r['mission_key']==register_mission(chosen_mission())]
    for scenario in get_scenario_defs()['scenarios']:
        rec=[dict(id=r['id'],cost_usd=r['scenarios'][scenario]['cost_usd'],CO2proxy_kg=r['scenarios'][scenario]['CO2proxy_kg']) for r in defaults]
        best=min(defaults,key=lambda r:r['scenarios'][scenario]['cost_usd'])
        frontier=pareto_frontier(rec)
        emin=min(r['CO2proxy_kg'] for r in rec);emax=max(r['CO2proxy_kg'] for r in rec)
        eps=[epsilon_cost_minimum(rec,emin+(emax-emin)*q/8) for q in range(9)]
        for row in eps:
            if row['feasible']:row['selected_policy_id']=rec[row['selected_index']]['id']
        out[scenario]=dict(min_cost_policy_id=best['id'],cost_environment_frontier_ids=[rec[i]['id'] for i in frontier],epsilon_rows=eps)
    central='central';cost_time=[]
    for a in defaults:
        if not any(b['habitation_upper_days']<=a['habitation_upper_days'] and b['scenarios'][central]['cost_usd']<=a['scenarios'][central]['cost_usd'] and (b['habitation_upper_days']<a['habitation_upper_days'] or b['scenarios'][central]['cost_usd']<a['scenarios'][central]['cost_usd']) for b in defaults):cost_time.append(a['id'])
    return out,cost_time


def run():
    REGISTRY.clear();MISSIONS.clear();configure_inputs()
    ms=mission_catalog();chosen=chosen_mission()
    half=next(m for m in ms if abs(m.get('release_speed_fraction',-1))<1e-12) if any('release_speed_fraction' in m for m in ms) else ms[0]
    # Use the endpoints of the nominal speed family, not a changed dry-mass case.
    half=min((m for m in ms if m.get('nominal_speed_family',False)),key=lambda m:m['initial_tangential_speed_km_s'],default=half)
    selected=[chosen]
    if mission_key(half)!=mission_key(chosen):selected.append(half)
    candidates=[];baselines=[];water_catalogues={};sizes=[]
    for m in selected:
      mk=register_mission(m)
      for mode in ['ideal','fault']:
        water=build_water_catalogue(mission=m,mode=mode);water_catalogues[mode+'_'+mk]=water
        shares=share_catalogue(mode,mk)
        sizes.append(dict(mission_key=mk,mode=mode,shares=shares,water_candidates=len(water),feasible_water=sum(z['feasible'] for z in water)))
        for share in shares:
            baselines.append(build_policy(share,water[0],0.,mode,mk,construction_only=True))
            for w in water:
                if not w['feasible']:continue
                for prep in [0.,.5,1.]:
                    for packing in ['capacity_fill','matched','single_item','module_two']:
                        candidates.append(build_policy(share,w,prep,mode,mk,packing_policy=packing))
    selection,costtime=select_and_frontiers(candidates)
    default_mk=register_mission(chosen);construction_summary=[]
    for mode in ['ideal','fault']:
        rows=[r for r in baselines if r['mode']==mode and r['mission_key']==default_mk]
        for route,rs in [('R',[r for r in rows if r['construction_E_share']==0]),('E',[r for r in rows if r['construction_E_share']==1]),('ER',[r for r in rows if 0<r['construction_E_share']<1])]:
            fastest=min(rs,key=lambda z:z['generic_construction_delivery_upper_days'])
            construction_summary.append(dict(mode=mode,route=route,policy_id=fastest['id'],E_share=fastest['construction_E_share'],delivery_upper_years=fastest['generic_construction_delivery_upper_days']/P,
                scenario_cost_USD=fastest['scenarios']['central']['cost_usd'],scenario_cost_interval_USD=fastest['scenarios']['central']['cost_interval_usd']))
    pure=[]
    for route in ['E','R']:
      for mode in ['ideal','fault']:
        rs=[r for r in candidates if r['mission_key']==default_mk and r['mode']==mode and r['construction_route']==route and r['preposition_E_share']==(1 if route=='E' else 0) and r['operation_route'] in [None,route]]
        b=min(rs,key=lambda r:r['scenarios']['central']['cost_usd']);pure.append(dict(route=route,mode=mode,policy_id=b['id']))
    deadlines=[]
    rows=[r for r in candidates if r['mode']=='fault' and r['mission_key']==default_mk]
    for years in [50,100,250,350,500,1000,1500]:
        ok=[r for r in rows if r['habitation_upper_days']<=years*P]
        b=min(ok,key=lambda r:r['scenarios']['central']['cost_usd']) if ok else None
        deadlines.append(dict(deadline_years=years,certified_candidates=len(ok),policy_id=b['id'] if b else None,
            scope='Feasibility of saved sufficient policies only; expansion is not silently introduced.'))
    best=next(r for r in rows if r['id']==selection['central']['min_cost_policy_id'])
    stock=min((r for r in rows if r['water_id']=='stock_all'),key=lambda r:r['scenarios']['central']['cost_usd'])
    crossing=compare_fixed_plans(best['features'],stock['features'])
    out=dict(version='v9_fixed_capacity_architecture_and_loss_model',date='2026-10-28',
        official_problem='evidence/2026_MCM_Problem_B.pdf',generic_construction_t=GENERIC_CONSTRUCTION_T,
        fixed_capacity=dict(harbours=3,lift_gross_t_year_each=179000.,selected_R_sites=10,R_flights_year_each=250,
            R_payload_t=125.,R_site_calendar_identity='Future250/year is a named scenario, not official supplied historical frequency.'),
        missions=MISSIONS,default_mission_key=default_mk,catalogue_sizes=sizes,
        water_catalogues=water_catalogues,construction_summary=construction_summary,
        construction_baselines=baselines,candidates=candidates,selections=selection,
        cost_time_frontier_ids=costtime,pure_complete_mission_selections=pure,deadline_stress=deadlines,
        cost_environment_definitions=get_scenario_defs(),best_vs_best_stock_fixed_plan_crossing=crossing,
        hardware_ledger='Generic100Mt plus ADDITIONAL water modules, dedicatedfresh/rawtanks and incrementalpowerhardware, delivered in late homogeneous-item campaigns. All potentially allocated full-job item manufacturing is charged, including destroyed or quarantined equipment; only the required installed quantities run.',
        power_hardware_design_scenario=dict(module_kW=POWER_MODULE_KW,dry_t=POWER_MODULE_DRY_T,
            spare_generation_modules_fault=1,
            service='Firm continuous electrical output including required heat rejection, distribution and conditioning; one generation module may be unavailable in fault mode. Not an unbuffered solar-nameplate rating.',
            source='NASA2024FSP40kW/under6t concept requirement, not a qualified installed product or a guarantee at100000-person scale.'),
        equipment_packing_catalogue=['capacity_fill','matched','single_item','module_two'],
        exogenous_capacity_prerequisite='By2050 each used apex warehouse and robotic Moon receiving service is contractually ready before its first cargo. Capacity prices reserve/procure those services; provider infrastructure deployment mass/time is outside this strategic model. Required ratings are outputs, not evidence of actual availability.',
        proof_scope='Finite declared architecture/share/preposition catalogue. Sufficient completion/service times, not global engineering optima or future forecasts. Separate ideal/fault supports preserve the same physical lift/site capacity.',
        unresolved=['Three-dimensional finite-thrust/SOI rendezvous and engine/structure validation',
            'Actual future manufacturing, O&M, renewal and mission prices',
            'Long-horizon maintained readiness of upfront spare hull inventory and other infrastructure',
            'Water quality, contamination isolation and component performance',
            'Unmodeled non-CO2, nuclear, land/ocean ecological and complete lifecycle impacts'],
        phase_registry_file='results/phases_v9.json')
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/joint_v9.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    save_phase_registry(ROOT/'results/phases_v9.json',REGISTRY)
    with (ROOT/'results/policy_summary_v9.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['id','mode','mission_key','construction_E_share','preposition_E_share','water_id','operation_route','eta','generic_construction_delivery_upper_days','habitation_upper_days','cost_USD_central','CO2proxy_kg_central']
        w=csv.DictWriter(f,fields);w.writeheader()
        for r in candidates:
            z={k:r[k] for k in fields if k in r};z.update(cost_USD_central=r['scenarios']['central']['cost_usd'],CO2proxy_kg_central=r['scenarios']['central']['CO2proxy_kg']);w.writerow(z)
    print(json.dumps(dict(policies=len(candidates),phases=len(REGISTRY),baselines=construction_summary,central_best=dict(id=best['id'],water=best['water_id'],Eshare=best['construction_E_share'],prepositionE=best['preposition_E_share'],cost_USD=best['scenarios']['central']['cost_usd'],habitation_upper_years=best['habitation_upper_days']/P)),ensure_ascii=False))
    return out


if __name__=='__main__':run()
