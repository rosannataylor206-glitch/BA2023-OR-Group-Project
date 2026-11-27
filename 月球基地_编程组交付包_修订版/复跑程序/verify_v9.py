"""Independent arithmetic and finite event-calendar checks of v9.

This verifier reconstructs the central bounds rather than accepting producer
flags. It certifies neither real hardware nor all schedules outside the stated
support and finite design catalogue.
"""
from pathlib import Path
import itertools
import json
import math
import hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
SCALAR_EXPECTATIONS={}


def count_bound(n,b,P):
    q,r=divmod(int(n),int(P))
    return int(b)*q+min(int(b),r)


def close(a,b,atol=1e-7,rtol=1e-10):
    if not math.isfinite(float(a)) or not math.isfinite(float(b)) or abs(a-b)>atol+rtol*max(abs(a),abs(b)):
        raise AssertionError((a,b))


def physics_check():
    import physics_v9 as p
    data=json.loads((ROOT/'results/physics_v9.json').read_text())
    cases=0
    for z in data['missions']:
        g=z['geometry'];r=g['apex_radius_km'];u=g['initial_tangent_speed_km_s'];R=p.MOON_DISTANCE
        h=r*u;energy=u*u/2-p.MU_E/r
        vt=h/R;vr=math.sqrt(max(0,2*(energy+p.MU_E/R)-vt*vt))
        vm=math.sqrt((p.MU_E+p.MU_M)/R)
        vinf=math.hypot(vr,vt-vm)
        close(vinf,g['moon_relative_v_infinity_km_s'])
        dv=abs(g['apex_corotation_speed_km_s']-u)+math.sqrt(vinf*vinf+2*p.MU_M/(p.R_M+100))-math.sqrt(p.MU_M/(p.R_M+100))
        close(dv,z['tug_delta_v_each_way_km_s'])
        dT=z['dry_tug_to_net_cargo_ratio'];dL=z['dry_lander_to_net_cargo_ratio']
        at=math.exp(dv/(p.G0_KM_S2*z['Isp_tug_s']))
        al=math.exp(z['lander_delta_v_each_way_km_s']/(p.G0_KM_S2*z['Isp_lander_s']))
        # Reconstruct from the final returned dry structures through each burn.
        return_prop=(dT+dL)*(at-1)
        pre_surface=al*(1+dL*al)
        wet=(pre_surface+dT+return_prop)*at
        close(wet,z['beta_outbound_per_net_cargo'])
        close(1+dL*al,z['landing_mass_per_net_cargo'])
        rawtail=z['return_cycle_unrounded_days_scenario']-z['outbound_ready_to_touchdown_days_scenario']
        close(rawtail,z['return_tail_unrounded_days_scenario'])
        assert z['return_tail_upper_days']>=rawtail-1e-10
        assert z['return_cycle_days']>=z['outbound_ready_to_touchdown_days_integer_scenario']+z['return_tail_upper_days']
        cases+=1
    nominal=[z for z in data['missions'] if z['study_group']=='nominal_21_speed_grid']
    best=min(nominal,key=lambda z:z['beta_outbound_per_net_cargo'])
    assert best['transfer_mode']=='free_release'
    assert len(nominal)==21
    return dict(independent_mass_and_velocity_records=cases,rounded_tail_composition_checked=True,
        finite_speed_grid_checked=21,scope='Independent algebra within the circular, impulsive, zero-SOI mission family.')


def scalar_certificate(c):
    P=c['P'];G=c['G'];eta=c['eta'];Q=c['Q'];delta=c['delta'];M=c['Lmax']+c['review_days']-1
    cap=c['R0']+c['Rc'];proc=c['R0']+c['Rp'];D=(1-eta)*G
    margin=Q*(1/delta-c['B']/P)-D-eta*G*cap/P-Q*c['J']/P-c['C']*c['tank_events']/P
    close(margin,c['transport_margin_t_day'])
    assert margin>0 and c['K']*(P-proc)>=eta*G*P-1e-7
    key=tuple(c[k] for k in ['P','G','eta','Q','delta','Lmax','K','B','R0','Rc','Rp','J','tank_events','C','review_days'])
    if key in SCALAR_EXPECTATIONS:
        close(SCALAR_EXPECTATIONS[key],c['reserve_t'],atol=2e-7)
        return 0
    H=math.lcm(P,delta);switch=P*math.ceil(proc/c['Rp']) if c['Rp'] else P
    n0=math.ceil((1+c['B'])/(1/delta-c['B']/P));start=max(M+n0,switch)
    best=-math.inf
    # Independently extend through ten extra cycles beyond the producer scan.
    for n in range(M,start+11*H+1):
        e1=eta*G*(count_bound(n,cap,P)+proc)
        e2=eta*G*max(proc,count_bound(n,c['R0'],P)+count_bound(n,c['Rc'],P)+count_bound(n,c['Rp'],P))
        A=D*n+min(e1,e2)+Q*count_bound(n,c['J'],P)+c['C']*count_bound(n,c['tank_events'],P)
        k=n-M;S=Q*max(0,k//delta-count_bound(k,c['B'],P))
        best=max(best,A-S)
    close(Q+best,c['reserve_t'],atol=2e-7)
    SCALAR_EXPECTATIONS[key]=Q+best
    return start+11*H-M+1


def receiver_check(rx):
    l=rx['upstream_min_days'];u=rx['upstream_max_days'];delta=rx['delta'];m=rx['receiver_slots'];P=rx['P'];B=rx['port_closed_budget']
    period=math.lcm(P,delta)
    val=max(math.ceil((n+u-l)/delta)-m*((n-1)-count_bound(n-1,B,P)) for n in range(1,11*period+1))
    assert val==rx['pre_service_queue_bound_flights']
    h=next(t for t in range(1,11*P+1) if m*(t-count_bound(t,B,P))>=val)
    assert u+h-1==rx['Lmax']


def suffix_envelope_small_calendars():
    # Independent recurrence at equality of the processing stability condition.
    checked=0;paths=0
    for P in [3,4]:
        opts=[tuple(int(i==k) for i in range(P)) for k in range(P)]+[(0,)*P]
        eta=.8;G=5.;a=eta*G;K=a*P/(P-2)
        for common,cap,proc in itertools.product(opts,repeat=3):
            for raw_loss_day in [-1,*range(P)]:
                for fraction in [0.,.4,1.]:
                    T=6*P;Y=0.;losses=[]
                    for t in range(T):
                        if t%P==raw_loss_day:Y=max(0,Y-.7*a)
                        capture=fraction if common[t%P] or cap[t%P] else 1.
                        losses.append(a*(1-capture))
                        Y=max(0,Y+a*capture-(0 if common[t%P] or proc[t%P] else K))
                        for n in range(1,t+2):
                            value=sum(losses[t-n+1:t+1])+Y
                            e1=a*(count_bound(n,2,P)+2)
                            e2=a*max(2,3*count_bound(n,1,P))
                            assert value<=min(e1,e2)+1e-8,(P,common,cap,proc,raw_loss_day,fraction,t,n,value,e1,e2)
                            checked+=1
                    paths+=1
    return dict(independent_fault_and_raw_loss_paths=paths,suffix_interval_checks=checked,
        scope='Complete stated small periodic binary calendars, three partial-capture levels and raw-loss phases; not all real histories.')


def queue_small_calendars():
    from collections import deque
    tested=0
    for delta,slots in [(1,2),(2,1)]:
        P=4;lower=1;upper=3;period=math.lcm(P,delta)
        bq=max(math.ceil((n+upper-lower)/delta)-slots*((n-1)-count_bound(n-1,1,P)) for n in range(1,period+1))
        h=next(t for t in range(1,20) if slots*(t-count_bound(t,1,P))>=bq);deadline=upper+h-1
        launches=list(range(0,4,delta))
        closures=[(0,)*P]+[tuple(int(t==k) for t in range(P)) for k in range(P)]
        for lagseq in itertools.product(range(lower,upper+1),repeat=len(launches)):
            for flags in closures:
                arrivals={};q=deque();worst=0
                for i,(t,lag) in enumerate(zip(launches,lagseq)):arrivals.setdefault(t+lag,[]).append((t,i))
                for t in range(4+deadline+P):
                    q.extend(arrivals.get(t,[]));assert len(q)<=bq
                    if not flags[t%P]:
                        for _ in range(min(slots,len(q))):
                            launch,i=q.popleft();worst=max(worst,t-launch);assert t-launch<=deadline
                assert not q
                tested+=1
    return dict(independent_small_arrival_and_closure_cases=tested)


def water_check():
    import water_v9 as w
    data=json.loads((ROOT/'results/water_v9.json').read_text())
    catalogues={mode:data[mode] for mode in ['ideal','fault']}
    components=0;scan_points=0
    for mode,rows in catalogues.items():
        ids={z['id'] for z in rows}
        for eta in [.94,.98]:
            assert any(z['eta']==eta and z['operation_route']=='R' for z in rows)
            assert any(z['eta']==eta and z['operation_route']=='E' for z in rows)
            assert any(z['eta']==eta and z['operation_route']=='ER' for z in rows)
        assert 'stock_all' in ids
        for z in rows:
            if not z['feasible']:continue
            power_limit=z['input_scenarios']['lunar_power_budget_kW']
            assert power_limit is None or z['plant_power_kW']<=power_limit+1e-8
            for c in z['components']:
                receiver_check(c['receiver']);scan_points+=scalar_certificate(c['certificate'])
                cert=c['certificate'];G=c['G_t_day'];P=cert['P'];H=z['water_horizon_days']
                assert c['reserve_t']>=cert['reserve_t']-1e-8
                close(c['fresh_capacity_required_t'],c['reserve_t']+G)
                assert c['raw_capacity_required_t']>=G*(cert['R0']+cert['Rp']+1)-1e-8
                input_=z['input_scenarios'];C=input_['tank_capacity_t'];b=cert['tank_events']
                assert (c['fresh_tank_compartments']-b)*C>=c['fresh_capacity_required_t']-1e-7
                assert (c['raw_tank_compartments']-b)*C>=c['raw_capacity_required_t']-1e-7
                external=(1-cert['eta'])*G*H+cert['eta']*G*count_bound(H,cert['R0']+cert['Rc'],P)+cert['Q']*count_bound(H,cert['J'],P)+cert['C']*count_bound(H,cert['tank_events'],P)
                assert c['annual_full_departures_upper']==math.floor(external/cert['Q']+1e-10)
                if c['route']=='R':
                    assert c['operating_R_sites']<=10
                    assert c['receiver_actual_flight_slots']==c['receiver']['receiver_slots']*c['flights_per_batch']
                    assert c['closed_budget']==P-c['nominal_R_open_dates']+(0 if mode=='ideal' else c['flights_per_batch']*input_['R_closed_days'])
                else:
                    import physics_v9 as ph
                    mission=ph.chosen_mission();cyc=c['receiver']['Lmax']+mission['return_tail_upper_days']
                    fc=c['fleet_certificate'];assert fc['cycle_days']>=cyc
                    assert fc['base_fleet']*cert['delta']>=cyc+input_['activation_days']
                components+=1
    return dict(independent_components=components,scalar_interval_points_including_extended_tails=scan_points,
        architecture_cross_product_checked=True,raw_loss_suffix_tests=suffix_envelope_small_calendars(),
        queue_tests=queue_small_calendars())


def construction_plan_check(z,mission=None):
    import physics_v9 as ph
    m=mission or ph.chosen_mission();x=z['inputs'];s=z['service'];P=x['period_days']
    dry=m['return_dry_per_net_cargo'];g=1+(m['beta_outbound_per_net_cargo']-dry-1)/(1-x['propellant_storage_loss_fraction'])
    al=1-x['lift_closed_days']/P;ap=1-x['port_closed_days']/P
    ae=1/x['E_delta_days']-x['E_closed_days']/P;ar=(x['rocket_flights_per_site_year']-x['R_closed_days'])/P
    lift=x['lift_t_year_per_harbour']/P*al
    re=min(lift/g,x['E_payload_t']*ae,x['E_payload_t']*ap)
    rr=min(x['R_payload_t']*ar,2*x['R_payload_t']*ap)
    tl=x['lift_closed_days']/al+1;te=(1+x['E_closed_days'])/ae+1;tr=(1+x['R_closed_days'])/ar+1;tp=(1+x['port_closed_days'])/ap+1
    close(s['recurring_lift_per_payload'],g);close(s['rE_t_day_per_harbour'],re);close(s['rR_t_day_per_site'],rr)
    close(s['Tlift_days'],tl);close(s['TdispatchE_days'],te);close(s['TdispatchR_days'],tr);close(s['Tport_days'],tp)
    close(s['E_path_latency_days'],tl+x['climber_transit_days']+te+s['E_delivery_upper_days']+tp)
    close(s['R_path_latency_days'],tr+x['direct_delivery_days']+tp)
    receiver_check(s['receiver_E']);receiver_check(s['receiver_R'])
    assert s['E_return_tail_upper_days']>=m['return_tail_unrounded_days_scenario']-1e-10
    base=math.ceil((s['receiver_E']['Lmax']+m['return_tail_upper_days']+x['hull_activation_days'])/x['E_delta_days'])
    assert s['base_hulls_per_harbour']==base
    delivered=0.;lift_total=0.;r_flights=0;new_hulls=0
    for route,p in z['routes'].items():
        if not p['active']:continue
        E=route=='E';n=x['harbours'] if E else x['rocket_sites'];Q=x['E_payload_t'] if E else x['R_payload_t'];r=re if E else rr
        J=x['cargo_losses_E_per_harbour_year'] if E else x['cargo_losses_R_per_site_year'];h=x['hull_losses_E_per_harbour_year'] if E else 0
        H=p['completion_upper_days'];T=s['E_path_latency_days'] if E else s['R_path_latency_days']
        available=p.get('available_intact_hulls_per_harbour',0) if E else 0
        base_deficit=max(0,base-available) if E else 0
        spare=math.ceil(h*H/P+h-1e-12) if h else 0
        needs=E and (base_deficit>0 or h>0)
        deploy=math.ceil(tl+x['climber_transit_days']+dry*Q*(base_deficit+spare)/lift) if needs else 0
        assert p['initial_deployment_days']==deploy
        d=math.floor(H-deploy-T);assert p['source_duration_days']==d and d>=0
        N=math.ceil(r*d/Q-1e-12);assert p['attempts_per_source']==N
        close(p['full_payload_t'],n*N*Q)
        lost=count_bound(H,J,P);h_lost=count_bound(H,h,P)
        guarantee=n*(max(0,r*d-4*Q)-Q*lost)
        close(p['guarantee_t'],guarantee);assert guarantee>=p['target_t']-1e-6
        assert p['cargo_loss_count_per_source_upper']==lost
        close(p['cargo_lost_t_upper'],n*Q*lost)
        assert p['actual_dispatch_cutoff_days']==H and p['no_dispatches_during_handoff']
        assert p['hull_losses_total_upper']==n*h_lost
        assert p['spare_hulls_per_harbour']==spare and spare>=h_lost
        a1=dry*Q*h/(P*lift) if E else 0
        a0=(tl+x['climber_transit_days']+dry*Q*(base_deficit+(h+1 if h else 0))/lift+1) if needs else 0
        slope=r*(1-a1)-Q*J/P;intercept=r*(a0+T+1)+4*Q+Q*J
        close(p['affine_net_rate_t_day_per_source'],slope)
        close(p['affine_intercept_t_per_source'],intercept)
        assert H==max(1,math.ceil((p['target_t']/n+intercept)/slope))
        assert guarantee/n>=slope*H-intercept-1e-6
        dry_mass=n*(base_deficit+spare)*dry*Q if E else 0
        new_lift=g*n*N*Q+dry_mass if E else 0
        close(p['initial_hull_mass_t'],dry_mass);close(p['new_lift_mass_t'],new_lift)
        if E:
            assert p['guaranteed_intact_base_after_handoff']==n*max(base,available)
            assert p['hulls_installed']==n*(base_deficit+spare)
            # The post-cutoff tail must include every pre-H dispatched mission.
            assert p['ready_after_flush_days']>=H+s['receiver_E']['Lmax']+m['return_tail_upper_days']+x['hull_activation_days']-1e-8
            close(p['quarantine_apex_gross_t_upper'],n*5*Q*g)
            min_store=g*(r*(tl+te)+2*Q)+max(base,available)*dry*Q+spare*dry*Q
            assert p['warehouse_required_t']>=n*min_store-1e-7
            assert p['warehouse_installed_capacity_t']>=p['warehouse_required_t']-1e-7
            lift_total+=new_lift;new_hulls+=p['hulls_installed']
        else:
            assert p['ready_after_flush_days']>=H+s['receiver_R']['Lmax']-1e-8
            r_flights+=n*N
        delivered+=guarantee
    close(delivered,z['guaranteed_delivered_t']);assert delivered>=z['target_t']-1e-6
    assert z['construction_completion_upper_days']==max(p['completion_upper_days'] for p in z['routes'].values())
    assert z['ready_for_water_days']==max(p['ready_after_flush_days'] for p in z['routes'].values())
    close(z['features']['E_lift_t'],lift_total);assert z['features']['R_launches']==r_flights
    assert z['features']['E_hulls']==new_hulls
    # Terminal reservations cover coincident complete flights, never only averages.
    slots=sum(p['terminal_slots_reserved'] for p in z['routes'].values())
    touch=sum(p['terminal_touchdown_t_open_day'] for p in z['routes'].values())
    unload=sum(p['terminal_unload_t_open_day'] for p in z['routes'].values())
    assert slots<=z['terminal_modules']*x['terminal_slots_per_module']
    assert touch<=z['terminal_modules']*x['terminal_touchdown_t_year_per_module']/P+1e-7
    assert unload<=z['terminal_modules']*x['terminal_unload_t_year_per_module']/P+1e-7
    return 1


def construction_check():
    from dataclasses import replace
    import construction_v9 as c
    checks=0;monotonic=0
    for target in [1.,1000.,1e6,1e8]:
        for share in [0.,.25,.5,.75,1.]:
            prev=None
            for mode,x in [('ideal',c.ideal_inputs()),('fault',c.ConstructionInputs())]:
                z=c.plan_construction(share,x,target_t=target);assert z['feasible']
                checks+=construction_plan_check(z)
                if prev is not None:
                    assert z['construction_completion_upper_days']>=prev['construction_completion_upper_days']
                    assert z['features']['R_launches']>=prev['features']['R_launches']
                    assert z['features']['E_lift_t']>=prev['features']['E_lift_t']-1e-5
                    monotonic+=1
                prev=z
    x=c.ConstructionInputs();baseline=c.plan_construction(0.,x)
    slow=c.plan_construction(0.,replace(x,rocket_flights_per_site_year=125))
    assert slow['construction_completion_upper_days']>baseline['construction_completion_upper_days']
    # The declared input must actually alter throughput, unlike v8's dead alias.
    close(slow['service']['rR_t_day_per_site'],x.R_payload_t*(125-x.R_closed_days)/365)
    fastE=c.plan_construction(1.,x)
    slowE=c.plan_construction(1.,replace(x,lift_t_year_per_harbour=x.lift_t_year_per_harbour/2))
    assert slowE['construction_completion_upper_days']>fastE['construction_completion_upper_days']
    reuse=c.plan_construction(.5,x,target_t=25000.,available_E_hulls_per_harbour=fastE['base_E_hulls_per_harbour_after_handoff'])
    checks+=construction_plan_check(reuse)
    return dict(independent_policy_certificates=checks,ideal_to_fault_monotonic_comparisons=monotonic,
        declared_capacity_parameters_respond=True,returned_base_reuse_case_checked=True,
        small_physical_queue_tests=construction_small_schedules(),
        scope='Independent affine, integer loss/replacement, full-source, fleet, cutoff and resource arithmetic; no all-policy earliest-time proof.')


def construction_small_schedules():
    """Full FIFO physical schedules, independently of rate-latency arithmetic."""
    from dataclasses import replace
    from collections import defaultdict,deque
    import construction_v9 as con
    import physics_v9 as phy
    P=4;opts=[-1,*range(P)];cases=0
    x=con.ConstructionInputs(period_days=P,harbours=1,rocket_sites=1,
        lift_t_year_per_harbour=1000.,rocket_flights_per_site_year=3,
        E_payload_t=2.,R_payload_t=2.,E_delta_days=2,
        lift_closed_days=1,E_closed_days=0,R_closed_days=1,port_closed_days=1,
        cargo_losses_E_per_harbour_year=1,cargo_losses_R_per_site_year=1,
        hull_losses_E_per_harbour_year=1,climber_transit_days=1,
        E_delivery_jitter_days=0,direct_delivery_days=2,hull_activation_days=1)
    mission=phy.chosen_mission()
    for route in ['E','R']:
        z=con.plan_construction(1. if route=='E' else 0.,x,mission,target_t=10.)
        p=z['routes'][route];s=z['service'];H=p['completion_upper_days'];Q=x.E_payload_t if route=='E' else x.R_payload_t
        d=p['source_duration_days'];dep=p['initial_deployment_days'];r=p['source_rate_t_day_per_source'];u=s['E_delivery_upper_days'] if route=='E' else x.direct_delivery_days
        # Exhaust all one-fault phases and the no-fault option. Nominal R
        # opportunity phase is also changed; its balanced calendar is explicit.
        for lift_phase,dispatch_phase,port_phase,loss_phase,nominal_phase in itertools.product(opts,opts,opts,opts,range(P)):
            if route=='E' and (dispatch_phase!=-1 or nominal_phase!=0):continue
            if route=='R' and lift_phase!=-1:continue
            earth_buffer=source_accum=apex=0.;lift_arrivals=defaultdict(float)
            raw_arrivals=defaultdict(list);queue=deque();useful=0.;attempts=0
            for t in range(H):
                if dep<=t<dep+d:
                    source_accum+=r
                    full=math.floor((source_accum+1e-10)/Q)
                    earth_buffer+=full*Q;source_accum-=full*Q
                    if t==dep+d-1 and source_accum>1e-9:
                        earth_buffer+=Q;source_accum=0.
                if route=='E':
                    apex+=lift_arrivals.pop(t,0.)
                    if t%P!=lift_phase:
                        open_net=x.lift_t_year_per_harbour/P/s['recurring_lift_per_payload']
                        shipped=min(earth_buffer,open_net);earth_buffer-=shipped
                        lift_arrivals[t+x.climber_transit_days]+=shipped
                    opportunity=t%x.E_delta_days==0
                    waiting=apex
                else:
                    k=t+nominal_phase
                    opportunity=((k+1)*x.rocket_flights_per_site_year//P-k*x.rocket_flights_per_site_year//P)==1
                    opportunity=opportunity and t%P!=dispatch_phase
                    waiting=earth_buffer
                if opportunity and waiting>=Q-1e-8:
                    if route=='E':apex-=Q
                    else:earth_buffer-=Q
                    raw_arrivals[t+u].append((t,t%P==loss_phase));attempts+=1
                queue.extend(raw_arrivals.pop(t,[]))
                if t%P!=port_phase:
                    for _ in range(min(1 if route=='E' else 2,len(queue))):
                        sent,lost=queue.popleft()
                        if not lost:useful+=Q
            assert attempts<=p['attempts_per_source'],(route,attempts,p['attempts_per_source'])
            assert useful>=p['guarantee_per_source_t']-1e-7,(route,H,lift_phase,dispatch_phase,port_phase,loss_phase,nominal_phase,useful,p['guarantee_per_source_t'])
            cases+=1
    return dict(full_fifo_source_lift_dispatch_receiving_calendar_cases=cases,
        scope='Complete stated four-day periodic fault phases, balanced R-calendar phases and independently simulated packetized FIFO queues; not all full-size histories.')


def cost_record_check(f,e):
    import cost_environment_v9 as ce
    assert not e['missing_features'],e['missing_features']
    assert e['supplied_feature_vector_complete']
    v=e['features'];coeff=e['coefficients']
    independent_quantities={
        'earth_electricity_USD_kWh':v['E_energy_kWh'],
        'lift_nonenergy_USD_kg':1000*v['E_new_lift_t'],
        'E_propellant_procurement_USD_kg':1000*v['E_propellant_t'],
        'R_flight_services_USD':v['R_launches'],
        'E_hull_manufacture_USD':v['E_hulls_initial'],
        'E_flight_overhaul_USD':v['E_flights'],
        'water_module_manufacture_USD':v['water_modules'],
        'tank_manufacture_USD':v['tanks'],
        'lunar_electricity_USD_kWh':v['lunar_energy_kWh'],
        'lunar_power_capacity_USD_kW':v['lunar_power_capacity_kW'],
        'warehouse_capacity_USD_t':v['warehouse_capacity_t'],
        'receiving_slot_capacity_USD':v['lunar_receiving_slots'],
        'harbour_annual_upkeep_USD':v['harbour_service_years'],
        'R_site_annual_upkeep_USD':v['R_site_service_years'],
        'E_hull_annual_upkeep_USD':v['hull_service_years'],
        'warehouse_annual_upkeep_USD_t':v['warehouse_t_years'],
        'receiving_slot_annual_upkeep_USD':v['receiving_slot_years'],
    }
    independent_env={
        'earth_grid_CO2_kg_kWh':v['E_energy_kWh'],
        'R_direct_launch_CO2_kg':v['R_launches'],
        'R_upstream_CO2_proxy_kg':v['R_launches'],
        'E_propellant_production_CO2_proxy_kg_kg':1000*v['E_propellant_t'],
        'lunar_energy_upstream_CO2_proxy_kg_kWh':v['lunar_energy_kWh'],
    }
    close(sum(q*coeff[k] for k,q in independent_quantities.items()),e['cost_usd'],atol=.05)
    close(sum(q*coeff[k] for k,q in independent_env.items()),e['CO2proxy_kg'],atol=.05)
    for bound,index in [('cost_interval_usd',0),('cost_interval_usd',1)]:
        close(sum(q*ce.COST_COEFFICIENTS[k][index+1] for k,q in independent_quantities.items()),e[bound][index],atol=.05)
    close(sum(q*ce.ENVIRONMENT_COEFFICIENTS[k][1] for k,q in independent_env.items()),e['emissions_proxy_interval_kg'][0],atol=.05)
    close(sum(q*ce.ENVIRONMENT_COEFFICIENTS[k][2] for k,q in independent_env.items()),e['emissions_proxy_interval_kg'][1],atol=.05)
    assert not e['future_coefficients_empirically_calibrated']
    assert not e['full_lifecycle_environmental_impact_known']
    return 1


def cost_functions_check():
    import cost_environment_v9 as ce
    a={k:0. for k in ce.FEATURE_ALIASES};b=dict(a)
    a.update(E_new_lift_t=125.,E_energy_kWh=2.4e6,E_propellant_t=100.,E_hulls_initial=10.,E_flights=100.,
        infrastructure_years=20.,warehouse_capacity_t=10000.,lunar_receiving_slots=4.,harbour_service_years=60.,
        hull_service_years=200.,warehouse_t_years=200000.,receiving_slot_years=80.)
    b.update(R_launches=10.,infrastructure_years=10.,R_site_service_years=20.,lunar_receiving_slots=4.,receiving_slot_years=40.)
    records=[];n=0
    for name in ce.get_scenario_defs()['scenarios']:
        for f in [a,b]:
            e=ce.evaluate_features(f,name);n+=cost_record_check(f,e)
            if name=='central':records.append(e)
    comparison=ce.compare_fixed_plans(a,b)
    diff=records[0]['cost_usd']-records[1]['cost_usd'];cross=comparison['crossing_coefficient']
    if cross is not None and cross>=0:
        aa=ce.evaluate_features(a,{'R_flight_services_USD':cross});bb=ce.evaluate_features(b,{'R_flight_services_USD':cross})
        close(aa['cost_usd'],bb['cost_usd'],atol=.05)
    quantities=[r['cost_feature_quantities'] for r in records]
    changes={k:quantities[0][k]-quantities[1][k] for k in ce.COST_COEFFICIENTS}
    lower=sum(v*ce.COST_COEFFICIENTS[k][1 if v>=0 else 2] for k,v in changes.items())
    upper=sum(v*ce.COST_COEFFICIENTS[k][2 if v>=0 else 1] for k,v in changes.items())
    close(lower,comparison['exact_difference_interval_usd'][0],atol=.05)
    close(upper,comparison['exact_difference_interval_usd'][1],atol=.05)
    toy=[dict(cost_usd=1.,CO2proxy_kg=4.),dict(cost_usd=2.,CO2proxy_kg=2.),dict(cost_usd=3.,CO2proxy_kg=3.),dict(cost_usd=4.,CO2proxy_kg=1.)]
    assert ce.pareto_frontier(toy)==[0,1,3]
    assert ce.epsilon_cost_minimum(toy,2.)['selected_index']==1
    assert not ce.epsilon_cost_minimum(toy,.5)['feasible']
    return dict(independent_dot_product_and_coefficient_box_records=n,shared_coefficient_difference_box_checked=True,
        fixed_plan_crossing_checked=True,finite_environment_epsilon_and_dominance_toys=True,
        scope='Listed parameterized terms and coefficient boxes, not empirical future prices or complete environmental impact.')


def _pareto_ids(records,x,y):
    groups={}
    for r in records:groups.setdefault(x(r),[]).append(r)
    best=math.inf;ids=set()
    for v,group in sorted(groups.items()):
        yy=min(map(y,group))
        if yy<best:
            ids.update(r['id'] for r in group if y(r)==yy)
        best=min(best,yy)
    return ids


def saved_water_catalogue_check(rows,mode,mission):
    checked=points=0
    for row in rows:
        if not row['feasible']:continue
        x=row['input_scenarios'];P=x['period_days'];H=x['water_horizon_days']
        for c in row['components']:
            cert=c['certificate'];receiver_check(c['receiver']);points+=scalar_certificate(cert)
            assert c['reserve_t']>=cert['reserve_t']-1e-8
            assert c['processor_K_t_day']>=cert['K']-1e-8
            assert (c['processing_modules']-(0 if mode=='ideal' else x['spare_processor_modules']))*x['module_t_day']>=cert['K']-1e-8
            close(c['plant_dry_t'],c['processing_modules']*x['module_dry_mass_t'])
            close(c['plant_power_kW'],c['processing_modules']*x['module_power_kW'])
            close(c['tank_hardware_t'],c['tank_compartments']*x['tank_dry_mass_t'])
            close(c['fresh_capacity_required_t'],c['reserve_t']+c['G_t_day'])
            assert c['raw_capacity_required_t']>=c['G_t_day']*(cert['R0']+cert['Rp']+1)-1e-8
            C=x['tank_capacity_t'];fail=cert['tank_events']
            assert (c['fresh_tank_compartments']-fail)*C>=c['fresh_capacity_required_t']-1e-7
            assert (c['raw_tank_compartments']-fail)*C>=c['raw_capacity_required_t']-1e-7
            if c['route']=='R':
                n=c['flights_per_batch'];assert n<=10
                assert cert['B']==P-x['R_nominal_open_days']+(0 if mode=='ideal' else n*x['R_closed_days'])
                assert cert['J']==(0 if mode=='ideal' else n*x['cargo_lost_batches'])
                assert c['receiver_actual_flight_slots']==n*c['receiver']['receiver_slots']
            else:
                cycle=c['receiver']['Lmax']+mission['return_tail_upper_days'];fc=c['fleet_certificate']
                assert fc['cycle_days']>=cycle
                assert fc['base_fleet']*c['delta']>=cycle+x['activation_days']
                assert fc['spare_hulls']>=count_bound(H,0 if mode=='ideal' else x['hull_losses'],P)
            ext=(1-cert['eta'])*cert['G']*H+cert['eta']*cert['G']*count_bound(H,cert['R0']+cert['Rc'],P)+cert['Q']*count_bound(H,cert['J'],P)+cert['C']*count_bound(H,cert['tank_events'],P)
            assert c['annual_full_departures_upper']==math.floor(ext/cert['Q']+1e-10)
            checked+=1
        if row['components']:
            close(sum(c['G_t_day'] for c in row['components']),x['gross_service_t_day'])
            assert row['operating_R_sites_required']==sum(c['operating_R_sites'] for c in row['components'])<=10
            for top,per in [('plant_power_kW','plant_power_kW'),('hardware_lunar_t','hardware_lunar_t'),('initial_lunar_packed_t','initial_lunar_packed_t'),('operating_R_flights','annual_R_flights'),('operating_E_new_lift_t','annual_E_cargo_newlift')]:
                close(row[top],sum(c[per] for c in row['components']))
    return checked,points


def catalogue_choice_check():
    import cost_environment_v9 as ce
    J=json.loads((ROOT/'results/joint_v9.json').read_text())
    candidates=J['candidates'];baselines=J['construction_baselines'];scenarios=list(J['cost_environment_definitions']['scenarios'])
    assert len({r['id'] for r in candidates})==len(candidates)
    policy_byid={r['id']:r for r in candidates};all_byid={**policy_byid,**{r['id']:r for r in baselines}}
    coverage=0;components=points=0
    for case in J['catalogue_sizes']:
        mode=case['mode'];mk=case['mission_key'];water=J['water_catalogues'][mode+'_'+mk]
        a,b=saved_water_catalogue_check(water,mode,J['missions'][mk]);components+=a;points+=b
        feasible=[w['id'] for w in water if w['feasible']]
        actual={(r['construction_E_share'],r['water_id'],r['preposition_E_share'],r['equipment_packing_policy']) for r in candidates if r['mode']==mode and r['mission_key']==mk}
        expected=set(itertools.product(case['shares'],feasible,[0.,.5,1.],['capacity_fill','matched','single_item','module_two']))
        assert actual==expected,(mode,mk,len(actual),len(expected))
        rb=[r for r in baselines if r['mode']==mode and r['mission_key']==mk]
        assert {r['construction_E_share'] for r in rb}==set(case['shares'])
        assert any(w['operation_route']=='R' and w['eta']==.98 and w['feasible'] for w in water)
        coverage+=len(actual)
    evaluated=0
    for r in candidates+baselines:
        for scenario in scenarios:
            e=ce.evaluate_features(r['features'],scenario);saved=r['scenarios'][scenario]
            for k in ['cost_usd','CO2proxy_kg']:close(saved[k],e[k],atol=.05)
            for k in ['cost_interval_usd','emissions_proxy_interval_kg']:
                for a,b in zip(saved[k],e[k]):close(a,b,atol=.05)
            evaluated+=cost_record_check(r['features'],e)
    rows=[r for r in candidates if r['mode']=='fault' and r['mission_key']==J['default_mission_key']]
    selection_groups=0;epsilon=0
    for scenario,selection in J['selections'].items():
        score=lambda r:r['scenarios'][scenario]
        minimum=min(score(r)['cost_usd'] for r in rows)
        close(score(policy_byid[selection['min_cost_policy_id']])['cost_usd'],minimum,atol=.05)
        frontier=_pareto_ids(rows,lambda r:score(r)['cost_usd'],lambda r:score(r)['CO2proxy_kg'])
        assert set(selection['cost_environment_frontier_ids'])==frontier
        for z in selection['epsilon_rows']:
            feasible=[r for r in rows if score(r)['CO2proxy_kg']<=z['emissions_budget_kg']]
            assert z['feasible']==bool(feasible)
            if feasible:
                chosen=policy_byid[z['selected_policy_id']]
                close(score(chosen)['cost_usd'],min(score(r)['cost_usd'] for r in feasible),atol=.05)
                assert score(chosen)['CO2proxy_kg']<=z['emissions_budget_kg']
            epsilon+=1
        selection_groups+=1
    expected_frontier=_pareto_ids(rows,lambda r:r['habitation_upper_days'],lambda r:r['scenarios']['central']['cost_usd'])
    assert set(J['cost_time_frontier_ids'])==expected_frontier
    for z in J['construction_summary']:
        route=z['route'];rr=[r for r in baselines if r['mode']==z['mode'] and r['mission_key']==J['default_mission_key'] and (r['construction_route']==route)]
        minimum=min(r['generic_construction_delivery_upper_days'] for r in rr)
        chosen=all_byid[z['policy_id']];close(chosen['generic_construction_delivery_upper_days'],minimum)
        close(z['delivery_upper_years'],minimum/365)
    for z in J['pure_complete_mission_selections']:
        p=policy_byid[z['policy_id']];route=z['route'];share=1. if route=='E' else 0.
        assert p['construction_route']==route and p['preposition_E_share']==share and p['operation_route'] in [None,route]
    for z in J['deadline_stress']:
        ok=[r for r in rows if r['habitation_upper_days']<=365*z['deadline_years']]
        assert len(ok)==z['certified_candidates']
        assert (z['policy_id'] is not None)==bool(ok)
        if ok:close(policy_byid[z['policy_id']]['scenarios']['central']['cost_usd'],min(r['scenarios']['central']['cost_usd'] for r in ok),atol=.05)
    # Engineering point minima and exclusions are reconstructed, not trusted.
    S=json.loads((ROOT/'results/sensitivity_v9.json').read_text())
    for name,digest in S['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    sensitivity_records=0
    for case in S['cases']:
        ident=case['point_id'];rr=[r for r in S['policies'] if r['sensitivity_point_id']==ident]
        water=S['water_catalogues'][ident];a,b=saved_water_catalogue_check(water,'fault',S['mission']);components+=a;points+=b
        assert len(rr)==case['policies_generated']
        for r in rr:
            power_ok=case['integrated_power_limit_kW'] is None or r['required_water_plant_power_kW']<=case['integrated_power_limit_kW']+1e-8
            wh_ok=case['integrated_warehouse_limit_t'] is None or r['features']['warehouse_capacity_t']<=case['integrated_warehouse_limit_t']+1e-8
            assert r['integrated_stress_feasible']==(power_ok and wh_ok)
            for scenario in scenarios:
                e=ce.evaluate_features(r['features'],scenario);saved=r['scenarios'][scenario]
                close(e['cost_usd'],saved['cost_usd'],atol=.05);close(e['CO2proxy_kg'],saved['CO2proxy_kg'],atol=.05)
                evaluated+=cost_record_check(r['features'],e)
            sensitivity_records+=1
        feasible=[r for r in rr if r['integrated_stress_feasible']]
        assert len(feasible)==case['integrated_feasible_policies']
        for scenario,choice in case['best_by_coefficient_scenario'].items():
            assert (choice is not None)==bool(feasible)
            if choice:
                assert choice['policy_id'] in {r['id'] for r in feasible}
                close(choice['cost_USD'],min(r['scenarios'][scenario]['cost_usd'] for r in feasible),atol=.05)
        selection_groups+=len(scenarios)
    assert len(S['cases'])==S['counts']['declared_unique_input_points']==19
    assert sensitivity_records==S['counts']['saved_policy_instances']
    # Recompute nested-limit monotonicity from independently reconstructed minima.
    nested=0
    for group in ['integrated_lunar_water_power_limit_kW','integrated_apex_warehouse_limit_t']:
        cases=sorted([c for c in S['cases'] if c['group']==group],key=lambda c:c['parameter_value'])
        for a,b in zip(cases,cases[1:]):
            for scenario in scenarios:
                x=a['best_by_coefficient_scenario'][scenario];y=b['best_by_coefficient_scenario'][scenario]
                assert x is None or (y is not None and y['cost_USD']<=x['cost_USD']+.05)
                nested+=1
    return dict(main_policy_cartesian_choices_checked=coverage,main_and_sensitivity_cost_records_checked=evaluated,
        unique_additional_water_scalar_intervals=points,all_mission_engineering_water_components_checked=components,
        finite_selection_groups_checked=selection_groups,environment_epsilon_queries_checked=epsilon,
        nested_limit_comparisons_checked=nested,sensitivity_policy_instances_checked=sensitivity_records,
        complete_route_and_packing_cross_product=True,ideal_fault_fixed_capacity_baselines_present=True,
        source_hashes_match=True,cost_time_and_cost_environment_frontiers_checked=True,
        scope='All saved finite candidates and coefficient scenarios; no unrestricted design-space optimum or empirical forecast.')


def main():
    from phase_audit_v9 import audit_integrated
    result=dict(version='v9_independent_audit',physics=physics_check(),water=water_check(),construction=construction_check(),cost_environment=cost_functions_check())
    result['integrated_phase_recurrences']=audit_integrated(route_checker=construction_plan_check,cost_checker=cost_record_check)
    result['catalogue_choices']=catalogue_choice_check()
    result['all_implemented_checks_pass']=True
    result['scope']='Independent finite arithmetic, event calendar, physical-accounting recurrence and complete saved-catalogue checks. No actual hardware, lifetime/readiness or future-price certification.'
    (ROOT/'results/independent_v9.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
