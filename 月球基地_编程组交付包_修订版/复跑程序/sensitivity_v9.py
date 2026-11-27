"""Coupled one-factor engineering studies on a common coarse policy catalogue.

Every input point is a named design/stress scenario.  Capacity changes are
kept separate from the original fixed-capacity baseline.  No probabilities,
empirical confidence ranges or all-architecture optimum are estimated.
"""
from dataclasses import asdict, replace
from pathlib import Path
import csv
import hashlib
import json
import math
import time

import joint_v9 as joint
from construction_v9 import ConstructionInputs
from water_v9 import WaterInputs, build_water_catalogue
from physics_v9 import chosen_mission
from registry_v9 import save_phase_registry

ROOT=Path(__file__).resolve().parent
PACKING_POLICIES=['matched','module_two']
PRODUCERS=['construction_v9.py','water_v9.py','physics_v9.py',
           'cost_environment_v9.py','joint_v9.py','registry_v9.py','sensitivity_v9.py']


def source_hashes():
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
            for name in PRODUCERS}


def declared_points():
    """Nineteen unique points, each changing one named engineering factor."""
    C=ConstructionInputs();W=WaterInputs()
    points=[dict(id='baseline',group='baseline',value='declared_defaults',C=C,W=W,
                 warehouse_limit_t=None,power_limit_kW=None)]
    def add(name,group,value,c=None,w=None,warehouse=None,power=None):
        points.append(dict(id=name,group=group,value=value,C=c or C,W=w or W,
                           warehouse_limit_t=warehouse,power_limit_kW=power))
    for factor in [1.,1.4]:
        add(f'demand_{factor:g}','service_water_demand_factor',factor,
            w=replace(W,gross_service_t_day=962.*factor))
    for flights in [150,365]:
        add(f'R_calendar_{flights}','R_nominal_open_days_per_site',flights,
            c=replace(C,rocket_flights_per_site_year=flights),
            w=replace(W,R_nominal_open_days=flights))
    for factor in [.5,1.5]:
        add(f'lift_capacity_{factor:g}','lift_capacity_counterfactual_factor',factor,
            c=replace(C,lift_t_year_per_harbour=179000.*factor),
            w=replace(W,lift_t_year_per_harbour=179000.*factor))
    for factor in [0.,1.5]:
        ckeys=['lift_closed_days','E_closed_days','R_closed_days','port_closed_days',
               'cargo_losses_E_per_harbour_year','cargo_losses_R_per_site_year',
               'hull_losses_E_per_harbour_year']
        wkeys=['lift_closed_days','E_closed_days','R_closed_days','port_closed_days',
               'common_fault_days','capture_only_fault_days','processor_only_fault_days',
               'cargo_lost_batches','hull_losses','tank_loss_incidents','spare_processor_modules']
        cx=replace(C,**{k:math.ceil(getattr(C,k)*factor) for k in ckeys})
        wx=replace(W,**{k:math.ceil(getattr(W,k)*factor) for k in wkeys})
        add(f'counted_faults_{factor:g}','counted_fault_budget_factor',factor,c=cx,w=wx)
    for loss in [0.,.2]:
        add(f'propellant_loss_{loss:g}','total_propellant_storage_loss_fraction',loss,
            c=replace(C,propellant_storage_loss_fraction=loss),
            w=replace(W,annual_propellant_loss_fraction=loss))
    for mass in [5.,50.]:
        add(f'module_mass_{mass:g}','processor_module_dry_mass_t',mass,
            w=replace(W,module_dry_mass_t=mass))
    for power in [4000.,5000.,8000.]:
        # Retain all hydraulic candidates first; impose the power cap on the
        # complete integrated record, so excluded records remain inspectable.
        add(f'power_limit_{power:g}','integrated_lunar_water_power_limit_kW',power,
            power=power)
    for warehouse in [250000.,1000000.,2000000.]:
        add(f'warehouse_limit_{warehouse:g}','integrated_apex_warehouse_limit_t',warehouse,
            warehouse=warehouse)
    assert len(points)==19
    return points


def common_share_catalogue(mkey):
    fine=joint.share_catalogue('fault',mkey)
    balancing=[s for s in fine if all(abs(s-k/20)>1e-10 for k in range(21))]
    return sorted(set([0.,.25,.5,.75,1.]+balancing))


def policy_parameter_fingerprint(point):
    # A capacity limit changes filtering, not the generated physical policies.
    return json.dumps([asdict(point['C']),asdict(point['W'])],sort_keys=True)


def summarize(point,policies,water_catalogue,shares):
    feasible=[r for r in policies if r['integrated_stress_feasible']]
    scenarios=list(joint.get_scenario_defs()['scenarios'])
    best={}
    for scenario in scenarios:
        if feasible:
            p=min(feasible,key=lambda r:(r['scenarios'][scenario]['cost_usd'],r['id']))
            best[scenario]=dict(policy_id=p['id'],water_id=p['water_id'],
                operation_route=p['operation_route'],eta=p['eta'],
                construction_E_share=p['construction_E_share'],
                preposition_E_share=p['preposition_E_share'],
                equipment_packing_policy=p['equipment_packing_policy'],
                cost_USD=p['scenarios'][scenario]['cost_usd'],
                CO2proxy_kg=p['scenarios'][scenario]['CO2proxy_kg'],
                habitation_upper_years=p['habitation_upper_days']/365,
                warehouse_capacity_t=p['features']['warehouse_capacity_t'],
                water_power_kW=p['required_water_plant_power_kW'])
        else:best[scenario]=None
    fastest=min(feasible,key=lambda r:(r['habitation_upper_days'],r['id'])) if feasible else None
    return dict(point_id=point['id'],group=point['group'],parameter_value=point['value'],
        construction_inputs=asdict(point['C']),water_inputs=asdict(point['W']),
        integrated_warehouse_limit_t=point['warehouse_limit_t'],
        integrated_power_limit_kW=point['power_limit_kW'],
        construction_shares=shares,preposition_shares=[0.,1.],equipment_packing_policies=PACKING_POLICIES,
        water_catalogue_count=len(water_catalogue),
        certified_water_candidates=sum(w['feasible'] for w in water_catalogue),
        policies_generated=len(policies),integrated_feasible_policies=len(feasible),
        integrated_excluded_policies=len(policies)-len(feasible),
        water_exclusions=[dict(id=w['id'],reason=w.get('reason')) for w in water_catalogue if not w['feasible']],
        best_by_coefficient_scenario=best,
        fastest_policy_id=fastest['id'] if fastest else None,
        fastest_habitation_upper_years=fastest['habitation_upper_days']/365 if fastest else None,
        scope='Best of the SAME declared coarse share/preposition/architecture catalogue at this point. Not the main finer-catalogue optimum, not a global or empirical optimum.')


def run():
    started=time.monotonic();before=source_hashes()
    mission=chosen_mission();mkey=joint.register_mission(mission)
    points=declared_points();cache={};registry={};cases=[];all_records=[];all_water={}
    for point in points:
        joint.configure_inputs(point['C'])
        fp=policy_parameter_fingerprint(point)
        if fp in cache:
            raw,water,shares=cache[fp]
        else:
            joint.REGISTRY.clear()
            water=build_water_catalogue(inputs=point['W'],mission=mission,mode='fault')
            shares=common_share_catalogue(mkey);raw=[]
            for share in shares:
                for w in water:
                    if not w['feasible']:continue
                    for prep in [0.,1.]:
                        for packing in PACKING_POLICIES:
                            raw.append(joint.build_policy(share,w,prep,'fault',mkey,packing_policy=packing))
            registry.update(joint.REGISTRY)
            cache[fp]=(raw,water,shares)
        records=[]
        for policy in raw:
            # Different points can have the same root policy id because the
            # source id describes choices. Keep a point-qualified identity.
            r=dict(policy);r['source_policy_id']=policy['id'];r['id']=point['id']+'__'+policy['id']
            r['sensitivity_point_id']=point['id']
            exclusions=[]
            if point['power_limit_kW'] is not None and r['required_water_plant_power_kW']>point['power_limit_kW']+1e-8:
                exclusions.append('Installed water-processing modules exceed the explicit integrated power limit')
            if point['warehouse_limit_t'] is not None and r['features']['warehouse_capacity_t']>point['warehouse_limit_t']+1e-8:
                exclusions.append('Integrated procured warehouse capacity, including all hull history and quarantine, exceeds the explicit total limit')
            r['integrated_stress_feasible']=not exclusions;r['integrated_stress_exclusions']=exclusions
            records.append(r)
        all_records.extend(records);all_water[point['id']]=water
        cases.append(summarize(point,records,water,shares))
    after=source_hashes()
    if before!=after:raise RuntimeError('Producer files changed during sensitivity run; discard and rerun after freeze')
    # Limits only remove candidates from the same generated physical catalogue;
    # optimal catalogue costs cannot worsen when the corresponding limit rises.
    nested=[]
    for group in ['integrated_lunar_water_power_limit_kW','integrated_apex_warehouse_limit_t']:
        rows=sorted((c for c in cases if c['group']==group),key=lambda c:c['parameter_value'])
        for a,b in zip(rows,rows[1:]):
            for scenario in joint.get_scenario_defs()['scenarios']:
                za=a['best_by_coefficient_scenario'][scenario];zb=b['best_by_coefficient_scenario'][scenario]
                passed=(za is None or (zb is not None and zb['cost_USD']<=za['cost_USD']+1e-4))
                nested.append(dict(group=group,scenario=scenario,lower_limit=a['parameter_value'],upper_limit=b['parameter_value'],passed=passed))
    assert all(c['passed'] for c in nested)
    counts=dict(declared_unique_input_points=len(points),unique_physical_catalogue_runs=len(cache),
        saved_policy_instances=len(all_records),saved_integrated_feasible_policy_instances=sum(r['integrated_stress_feasible'] for r in all_records),
        unique_phase_certificates=len(registry),nested_limit_checks=len(nested))
    out=dict(version='v9_coupled_engineering_sensitivity',date='2026-10-28',counts=counts,
        source_sha256=before,producer_sources_unchanged=True,mission=mission,mission_key=mkey,
        cases=cases,policies=all_records,water_catalogues=all_water,
        nested_resource_checks=nested,phase_registry_file='results/sensitivity_phases_v9.json',
        coefficient_scenarios=joint.get_scenario_defs(),
        input_identity='All varied future capacities, device metrics, faults, losses and limits are declared scenarios. Lift changes are counterfactual capacity changes, not silently substituted for the fixed official baseline.',
        zero_fault_identity='The factor0 point removes counted operational faults and spare-module outages while retaining the separately declared transport jitter and propellant-retention scenario; it is not the main ideal-mode baseline.',
        catalogue_identity='Common coarse decision family: shares0,.25,.5,.75,1 plus the point-specific affine balancing share, preposition routesE orR, the matched and module_two homogeneous equipment packing rules, and all fifteen declared water architectures with explicit failures retained. The main catalogue also compares two other packing rules; its minima must not be conflated with this coarser sensitivity study. The fixed-two module rule is feasible at all tested5/20/50t module masses, preserving that same packing alternative when mass decreases.',
        interpretation='One-factor study around the same declared defaults. It does not cover every parameter interaction. A catalogue without certified policies is not a physical impossibility theorem. Cost units are the same illustrative coefficient scenarios, not empirical quotations or confidence intervals.',
        elapsed_seconds=time.monotonic()-started)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/sensitivity_v9.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    save_phase_registry(ROOT/'results/sensitivity_phases_v9.json',registry)
    fields=['point_id','group','parameter_value','policies_generated','integrated_feasible_policies','scenario','water_id','construction_E_share','preposition_E_share','equipment_packing_policy','cost_USD','habitation_upper_years','warehouse_capacity_t','water_power_kW']
    with (ROOT/'results/sensitivity_v9.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fields);writer.writeheader()
        for case in cases:
            for scenario,selection in case['best_by_coefficient_scenario'].items():
                row={k:case[k] for k in fields if k in case};row['scenario']=scenario
                if selection:row.update({k:selection[k] for k in fields if k in selection})
                writer.writerow(row)
    joint.configure_inputs()
    print(json.dumps(dict(counts=counts,all_nested_checks_pass=True,elapsed_seconds=out['elapsed_seconds']),ensure_ascii=False))
    return out


if __name__=='__main__':run()
