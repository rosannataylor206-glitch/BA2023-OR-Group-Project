"""Independent replay of saved phase histories and physical feature totals.

No call is made to joint_v9.build_policy or its state-update helpers.  Route
certificate arithmetic is delegated to the independently written checker in
verify_v9 through an optional callback.  Ready-service engineering conditions
remain conditions, rather than being asserted true by arithmetic.
"""
from pathlib import Path
import gc
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent


def close(a,b,label='',atol=1e-5):
    if not math.isclose(float(a),float(b),rel_tol=3e-11,abs_tol=atol):
        raise AssertionError((label,a,b))


def load_registry(path):
    try:
        from registry_v9 import load_phase_registry
    except ImportError:
        data=json.loads(Path(path).read_text(encoding='utf-8'))
        if 'phases' not in data:return data
        phases=data['phases'];trans=data.get('transports',data.get('transport_registry',{}))
        for phase in phases.values():
            for entry in phase.get('entries',[]):
                if 'transport_ref' in entry:entry['transport']=trans[entry.pop('transport_ref')]
        return phases
    return load_phase_registry(path)


def blank():
    return dict(day=0.,available=[0]*3,ever=[0]*3,quarantine=[0.]*3,
        warehouse=[0.]*3,harbour_first=[None]*3,site_first=[None]*10,
        hull_installs=[],warehouse_installs=[],terminal_installs=[],terminal=0,
        lift=0.,prop=0.,Ef=0,Rf=0,hulls=0,manufactured={},cargo_loss=0.,
        hull_loss=0,ground_quarantine=0.)


def add_warehouse(s,hub,need,now):
    cap=math.ceil(max(0.,need)/50000.-1e-12)*50000.
    if cap>s['warehouse'][hub]:
        s['warehouse_installs'].append((cap-s['warehouse'][hub],now))
        s['warehouse'][hub]=cap


def add_terminal(s,slots,touch,unload,now):
    n=max(math.ceil(slots/4),math.ceil(touch/(1e6/365)),math.ceil(unload/(1e6/365)))
    if n>s['terminal']:
        s['terminal_installs'].append((4*(n-s['terminal']),now));s['terminal']=n


def water_for(record,catalogues):
    # Main uses mode+mission; engineering studies use the point identifier.
    key=record.get('sensitivity_point_id') or record['mode']+'_'+record['mission_key']
    rows=catalogues[key]
    matches=[z for z in rows if z['id']==record['water_id']]
    assert len(matches)==1
    return matches[0]


def replay_record(record,phases,mission,water,*,construction_only=False,
                  route_checker=None,cost_checker=None,checked_routes=None):
    s=blank();dry=500.*mission['return_dry_per_net_cargo'];ids=record['phase_ids']
    assert ids and len(ids)==len(set(ids)),record['id']
    seen_items={};first_delivery=0.;first_ready=None;last_lift_kwh=None
    initial_water_delivered=False
    needed=dict(water_modules=water['processing_modules'],fresh_tanks=water['fresh_tank_compartments'],raw_tanks=water['raw_tank_compartments'],power_modules=(math.ceil(water['plant_power_kW']/40)+(1 if record['mode']=='fault' else 0)) if water['plant_power_kW']>0 else 0)
    item_checks=entries_checked=0;cshared=None
    for index,pid in enumerate(ids):
        p=phases[pid];close(p['start_day'],s['day'],'phase chronology')
        assert p['mission_key']==record['mission_key'] and p['mode']==record['mode']
        now=s['day']
        if p['kind']=='transport':
            duration=slots=touch=unload=0.;made=delivered=0
            actual_targets=[0.,0.,0.];rt=0.
            seen_hubs=set();seen_R=False
            if index==0:
                assert p['label']=='generic_100Mt_construction'
                close(sum(p['E_targets_t'])+p['R_target_t'],1e8,'generic target')
                close(sum(p['E_targets_t']),record['construction_E_share']*1e8)
                assert p['item_kind'] is None
            for e in p['entries']:
                z=e['transport'];r=z['routes'][e['route']];x=z['inputs'];service=z['service']
                assert r['active'] and z['feasible']
                common={k:v for k,v in x.items() if k not in ['harbours','rocket_sites']}
                if cshared is None:cshared=common
                else:assert common==cshared,'A source changed its physical/fault contract between phases'
                if checked_routes is not None and route_checker is not None:
                    # A losslessly shared transport object is checked once.
                    key=(id(z),record['mission_key'])
                    if key not in checked_routes:
                        route_checker(z,mission);checked_routes.add(key)
                entries_checked+=1
                duration=max(duration,z['ready_for_water_days'])
                if index==0:first_delivery=max(first_delivery,z['construction_completion_upper_days'])
                slots+=r['terminal_slots_reserved'];touch+=r['terminal_touchdown_t_open_day'];unload+=r['terminal_unload_t_open_day']
                last_lift_kwh=x['lift_kWh_kg']
                if e['route']=='E':
                    i=e['hub'];assert i in [0,1,2]
                    assert i not in seen_hubs,'A physical E harbour was allocated twice in one parallel stage'
                    seen_hubs.add(i)
                    assert x['harbours']==1 and x['rocket_sites']==10
                    close(e['available_before'],s['available'][i]);close(e['ever_hulls_before'],s['ever'][i])
                    base=service['base_hulls_per_harbour']
                    new=max(0,base-s['available'][i])+r['spare_hulls_per_harbour']
                    assert new==r['hulls_installed']
                    if s['harbour_first'][i] is None:s['harbour_first'][i]=now
                    s['ever'][i]+=new;s['hulls']+=new;s['hull_installs'].append((new,now))
                    s['available'][i]=max(s['available'][i],base)
                    # Reconstruct stream bound independently from rate/latency,
                    # rather than treating producer warehouse total as evidence.
                    stream=service['recurring_lift_per_payload']*max(
                        r['source_rate_t_day_per_source']*(service['Tlift_days']+service['TdispatchE_days'])+1000.,2500.)
                    quarantine=2500.*service['recurring_lift_per_payload']
                    need=s['ever'][i]*dry+s['quarantine'][i]+max(stream,quarantine)
                    close(e['warehouse_required_with_history_t'],need,'warehouse history')
                    add_warehouse(s,i,need,now)
                    s['quarantine'][i]+=quarantine
                    s['lift']+=r['new_lift_mass_t']
                    s['prop']+=(service['recurring_lift_per_payload']-1)*r['full_payload_t']
                    s['Ef']+=r['attempts_total'];s['hull_loss']+=r['hull_losses_total_upper']
                    actual_targets[i]=r['target_t'];Q=500.
                else:
                    assert not seen_R,'The ten R sites were allocated twice in one parallel stage'
                    seen_R=True
                    assert e['route']=='R' and x['rocket_sites']==10 and x['harbours']==3
                    rt+=r['target_t'];Q=125.
                    for i in range(10):
                        if s['site_first'][i] is None:s['site_first'][i]=now
                    s['Rf']+=r['attempts_total'];s['ground_quarantine']+=10*5*Q
                s['cargo_loss']+=r['cargo_lost_t_upper']
                if p['item_kind']:
                    b=e['item_units_per_full_job'];mass=p['item_unit_t']
                    assert isinstance(b,int) and 1<=b<=math.floor(Q/mass+1e-12)
                    close(b*mass,min(b*mass,Q),'manifest mass')
                    count=math.ceil(r['guarantee_t']/Q-1e-9)*b
                    assert count==e['guaranteed_item_units']
                    made+=r['attempts_total']*b;delivered+=count;item_checks+=1
            for a,b in zip(actual_targets,p['E_targets_t']):close(a,b,'source target')
            close(rt,p['R_target_t'],'R target')
            close(duration,p['duration_upper_days'],'parallel upper time')
            close(slots,p['terminal_slots']);close(touch,p['terminal_touchdown_t_open_day']);close(unload,p['terminal_unload_t_open_day'])
            add_terminal(s,slots,touch,unload,now)
            if p['item_kind']:
                kind=p['item_kind'];assert kind not in seen_items
                assert not initial_water_delivered,'Critical equipment arrived after the initial-water stage'
                expected_mass={'water_modules':water['input_scenarios']['module_dry_mass_t'],
                    'fresh_tanks':water['input_scenarios']['tank_dry_mass_t'],
                    'raw_tanks':water['input_scenarios']['tank_dry_mass_t'],
                    'power_modules':6.}[kind]
                close(p['item_unit_t'],expected_mass,'physical equipment unit mass')
                assert delivered>=p['item_required'];assert made==p['item_manufactured_upper']
                seen_items[kind]=p['item_required'];s['manufactured'][kind]=made
            if p['label']=='initial_usable_water':
                assert not initial_water_delivered
                for kind,n in needed.items():assert seen_items.get(kind,0)==n,(kind,n,seen_items)
                initial_water_delivered=True
                close(sum(p['E_targets_t'])+p['R_target_t'],water['initial_lunar_packed_t'])
            s['day']+=duration
            if index==0:first_ready=s['day']
        elif p['kind']=='apex_water_staging':
            assert not construction_only and initial_water_delivered
            Ecomponents=[c for c in water['components'] if c['route']=='E']
            assert len(Ecomponents)==len(p['components'])==1
            c=Ecomponents[0];duration=0.
            for d in p['components']:
                i=d['hub'];assert i==0
                base=c['operating_E_base_fleet'];spare=c['operating_E_spare_hulls']
                close(d['available_intact_before'],s['available'][i]);close(d['ever_hulls_before'],s['ever'][i])
                new=max(0,base-s['available'][i])+spare;assert new==d['new_hulls']
                s['available'][i]=max(s['available'][i],base)
                s['ever'][i]+=new;s['hulls']+=new;s['hull_installs'].append((new,now))
                if s['harbour_first'][i] is None:s['harbour_first'][i]=now
                mass=c['apex_stock_gross_t']+new*dry
                wx=water['input_scenarios']
                loss=0. if record['mode']=='ideal' else wx['annual_propellant_loss_fraction']
                recurring=1+(mission['beta_outbound_per_net_cargo']-mission['return_dry_per_net_cargo']-1)/(1-loss)
                close(c['apex_stock_gross_t'],c['annual_E_departures']*c['Qpacked']*recurring,'annual E stock')
                assert cshared is not None
                a=1-cshared['lift_closed_days']/cshared['period_days']
                rate=cshared['lift_t_year_per_harbour']/cshared['period_days']*a
                latency=cshared['lift_closed_days']/a+1+cshared['climber_transit_days']
                close(d['fixed_gross_lift_t_day'],rate,'one actual harbour lift')
                close(d['lift_and_climber_latency_days'],latency,'operating staging latency')
                need=s['ever'][i]*dry+s['quarantine'][i]+c['apex_stock_gross_t']
                close(d['total_new_lift_t'],mass);close(d['warehouse_requirement_t'],need)
                close(d['staged_new_mass_t'],c['apex_stock_gross_t']);close(d['dry_mass_per_hull_t'],dry)
                add_warehouse(s,i,need,now)
                days=math.ceil(d['lift_and_climber_latency_days']+mass/d['fixed_gross_lift_t_day'])
                assert days==d['duration_upper_days'];duration=max(duration,days)
                s['lift']+=mass;s['prop']+=c['apex_stock_gross_t']-c['annual_E_packed_cargo_t'];s['Ef']+=c['annual_E_departures']
            close(duration,p['duration_upper_days']);s['day']+=duration
        else:raise AssertionError(('Unknown phase',p['kind']))
    close(first_delivery,record['generic_construction_delivery_upper_days'])
    close(first_ready,record['generic_construction_ready_days'])
    close(s['day']-first_ready,record['additional_preposition_upper_days'])
    for key,actual in [('warehouse_capacity_per_harbour_t',s['warehouse']),('guaranteed_intact_E_base_at_operation',s['available']),('E_hulls_ever_deployed',s['ever']),('quarantined_apex_mass_per_harbour_t',s['quarantine'])]:
        for a,b in zip(record[key],actual):close(a,b,key)
    close(record['quarantined_R_ground_payload_t'],s['ground_quarantine'])
    close(record['construction_cargo_loss_upper_t'],s['cargo_loss']);close(record['construction_hull_loss_upper'],s['hull_loss'])
    assert record['purchased_equipment_upper']==s['manufactured']
    if not construction_only:
        close(record['habitation_upper_days'],s['day'])
        assert initial_water_delivered
        for kind,n in needed.items():assert seen_items.get(kind,0)==n,(kind,n,seen_items)
        for key,wkey in [('installed_water_modules','processing_modules'),('installed_fresh_tanks','fresh_tank_compartments'),('installed_raw_tanks','raw_tank_compartments'),('required_water_plant_power_kW','plant_power_kW')]:close(record[key],water[wkey])
        add_terminal(s,water['receiver_actual_flight_slots'],water['receiver_touchdown_t_per_open_day'],water['receiver_unload_t_per_open_day'],s['day'])
        for i in range(water['operating_R_sites_required']):
            if s['site_first'][i] is None:s['site_first'][i]=s['day']
        assert water['operating_R_sites_required']<=10
        # Optional explicit tail is introduced by the root to charge readiness
        # through the final dispatch's resolution/return after the water year.
        tail=record.get('operation_settlement_tail_upper_days',0.)
        service_end=s['day']+water['water_horizon_days'];end=service_end+tail
        if 'water_service_end_upper_days' in record:close(record['water_service_end_upper_days'],service_end)
        expected_tail=max([0.]+[c['fleet_certificate']['rotation_hold_days'] if c['route']=='E' else c['receiver']['Lmax'] for c in water['components']])
        if 'operation_settlement_tail_upper_days' in record:close(tail,expected_tail)
        hours=24*(water['water_horizon_days']+tail)
    else:
        assert not seen_items and record['habitation_upper_days'] is None
        end=s['day'];hours=0.
    close(record['policy_end_upper_days'],end)
    made=s['manufactured']
    f=dict(E_new_lift_t=s['lift'],E_energy_kWh=s['lift']*1000*last_lift_kwh,
        E_propellant_t=max(0.,s['prop']),R_launches=s['Rf']+(0 if construction_only else water['operating_R_flights']),
        E_hulls_initial=s['hulls'],E_flights=s['Ef'],water_modules=made.get('water_modules',0),
        tanks=made.get('fresh_tanks',0)+made.get('raw_tanks',0),lunar_energy_kWh=water['plant_power_kW']*hours,
        lunar_power_capacity_kW=made.get('power_modules',0)*40.,warehouse_capacity_t=sum(s['warehouse']),
        lunar_receiving_slots=4*s['terminal'],active_harbours=sum(t is not None for t in s['harbour_first']),
        active_R_sites=sum(t is not None for t in s['site_first']),infrastructure_years=end/365,
        harbour_service_years=sum((end-t)/365 for t in s['harbour_first'] if t is not None),
        R_site_service_years=sum((end-t)/365 for t in s['site_first'] if t is not None),
        hull_service_years=sum(n*(end-t)/365 for n,t in s['hull_installs']),
        warehouse_t_years=sum(n*(end-t)/365 for n,t in s['warehouse_installs']),
        receiving_slot_years=sum(n*(end-t)/365 for n,t in s['terminal_installs']))
    assert set(f)==set(record['features'])
    for k,v in f.items():close(record['features'][k],v,'feature '+k,atol=.1)
    if cost_checker is not None:
        from cost_environment_v9 import evaluate_features
        cost_checker(f,evaluate_features(f))
    return dict(phase_entries=entries_checked,critical_item_entries=item_checks)


def audit_policy_records(records,phases,missions,water_catalogues,*,construction_only=False,
                         route_checker=None,cost_checker=None,checked_routes=None):
    totals=dict(policy_records=0,phase_entries=0,critical_item_entries=0)
    checked_routes=checked_routes if checked_routes is not None else set()
    for r in records:
        water=water_for(r,water_catalogues)
        z=replay_record(r,phases,missions[r['mission_key']],water,construction_only=construction_only,
            route_checker=route_checker,cost_checker=cost_checker,checked_routes=checked_routes)
        totals['policy_records']+=1
        for k in z:totals[k]+=z[k]
    return totals


def audit_integrated(route_checker=None,cost_checker=None):
    J=json.loads((ROOT/'results/joint_v9.json').read_text(encoding='utf-8'))
    phases=load_registry(ROOT/J['phase_registry_file']);checked=set()
    main=audit_policy_records(J['candidates'],phases,J['missions'],J['water_catalogues'],route_checker=route_checker,cost_checker=cost_checker,checked_routes=checked)
    baselines=audit_policy_records(J['construction_baselines'],phases,J['missions'],J['water_catalogues'],construction_only=True,route_checker=route_checker,cost_checker=cost_checker,checked_routes=checked)
    route_count=len(checked);del phases,J,checked;gc.collect()
    S=json.loads((ROOT/'results/sensitivity_v9.json').read_text(encoding='utf-8'))
    phases=load_registry(ROOT/S['phase_registry_file']);checked=set()
    sens=audit_policy_records(S['policies'],phases,{S['mission_key']:S['mission']},S['water_catalogues'],route_checker=route_checker,cost_checker=cost_checker,checked_routes=checked)
    return dict(main=main,construction_baselines=baselines,sensitivity=sens,
        unique_route_object_checks=route_count+len(checked),
        scope='Independent saved phase-history recurrence, homogeneous item identities, fleet credit, quarantine and warehouse peaks, manufacturing/full-job features, phase timing and exposure composition. External ready-service and century-maintenance assumptions are not physically certified.')


if __name__=='__main__':print(json.dumps(audit_integrated(),ensure_ascii=False,indent=2))
