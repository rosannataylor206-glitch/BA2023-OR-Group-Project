"""Finite-year service water with a symmetric transport-architecture catalogue.

The catalogue is deliberately finite.  It includes the direct-rocket recycling
candidate omitted from v8, the elevator candidate, and two independently
protected service zones using one route each.  It is not an all-policy optimum.
All future plant, storage, calendar and fault figures are named design inputs.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, deque
import math
import json

from reference.water_v8 import certificate, receiver_bound, size_processor, fleet_bound, budget

ROOT = Path(__file__).resolve().parent

# Packed usable-water fraction (team assumption, not official problem data).
# Reading: of a 125 t nominal payload, 103.618 t is counted as usable fresh
# water; the remainder is packaging and fixture mass.  The value is a declared
# design scenario, so it is exposed as a WaterInputs field (below) and this
# constant only supplies the default used by earlier exports.
DEFAULT_PACKED_WATER_FRACTION = 103.618 / 125.
PACKED_WATER_FRACTION = DEFAULT_PACKED_WATER_FRACTION  # retained for compatibility

# Single accounting convention shared with joint_v9.py: the generic 100 Mt
# construction target is general building material only.  Water processors,
# tanks and incremental power hardware are a separate late-delivered increment
# and are never netted out of (or double counted inside) the generic target.
HARDWARE_ACCOUNTING = 'generic_100Mt_excludes_water_hardware__water_hardware_is_additional'


@dataclass(frozen=True)
class WaterInputs:
    gross_service_t_day: float = 962. * 1.2
    water_horizon_days: int = 365
    period_days: int = 365
    module_t_day: float = 25.
    module_dry_mass_t: float = 20.
    module_power_kW: float = 100.
    tank_capacity_t: float = 1000.
    tank_dry_mass_t: float = 10.
    lunar_power_budget_kW: float | None = None
    E_payload_t: float = 500.
    R_payload_t: float = 125.
    R_nominal_open_days: int = 250
    direct_delivery_days: int = 30
    direct_touchdown_ratio: float = 1.5
    E_jitter_days: int = 19
    lift_t_year_per_harbour: float = 179000.
    lift_closed_days: int = 30
    climber_transit_days: int = 30
    E_closed_days: int = 60
    R_closed_days: int = 60
    port_closed_days: int = 7
    common_fault_days: int = 7
    capture_only_fault_days: int = 3
    processor_only_fault_days: int = 3
    cargo_lost_batches: int = 1  # Per R site, or per selected E harbour, per P days.
    hull_losses: int = 1
    tank_loss_incidents: int = 1
    spare_processor_modules: int = 1
    activation_days: int = 2
    annual_propellant_loss_fraction: float = .05
    # Usable fresh water per tonne of nominal packed water (0, 1]; team assumption.
    packed_water_fraction: float = DEFAULT_PACKED_WATER_FRACTION
    apex_warehouse_capacity_t: float | None = None


def _validate(x):
    positive = ['gross_service_t_day', 'module_t_day', 'tank_capacity_t',
                'E_payload_t', 'R_payload_t', 'lift_t_year_per_harbour']
    nonnegative = ['module_dry_mass_t', 'module_power_kW', 'tank_dry_mass_t',
                   'direct_touchdown_ratio']
    for key in positive:
        val = getattr(x, key)
        if not math.isfinite(val) or val <= 0:
            raise ValueError(key + ' must be finite and positive')
    for key in nonnegative:
        val = getattr(x, key)
        if not math.isfinite(val) or val < 0:
            raise ValueError(key + ' must be finite and nonnegative')
    for key in ['lunar_power_budget_kW','apex_warehouse_capacity_t']:
        val=getattr(x,key)
        if val is not None and (not math.isfinite(val) or val<=0):
            raise ValueError(key+' must be None or finite and positive')
    integer_fields = ['water_horizon_days', 'period_days', 'R_nominal_open_days',
        'direct_delivery_days', 'E_jitter_days', 'lift_closed_days',
        'climber_transit_days', 'E_closed_days', 'R_closed_days',
        'port_closed_days', 'common_fault_days', 'capture_only_fault_days',
        'processor_only_fault_days', 'cargo_lost_batches', 'hull_losses',
        'tank_loss_incidents', 'spare_processor_modules', 'activation_days']
    for key in integer_fields:
        val = getattr(x, key)
        if isinstance(val, bool) or not math.isfinite(val) or int(val) != val or val < 0:
            raise ValueError(key + ' must be a nonnegative integer')
    if min(x.water_horizon_days, x.period_days, x.direct_delivery_days) <= 0:
        raise ValueError('Positive horizon, period and direct transit required')
    if x.water_horizon_days > x.period_days:
        raise ValueError('This catalogue protects at most one period; extend storage repairs explicitly for longer horizons')
    if not 0 < x.R_nominal_open_days <= x.period_days:
        raise ValueError('Nominal R calendar must have 1..P open dates')
    if not 0 <= x.annual_propellant_loss_fraction < 1:
        raise ValueError('Propellant fractional loss must be in [0,1)')
    if not 0 < x.packed_water_fraction <= 1:
        raise ValueError('Usable water per packed tonne must be in (0,1]')


def _mission(mission):
    if mission is not None:
        return mission
    from physics_v9 import chosen_mission
    return chosen_mission()


def _budgets(x, mode):
    if mode not in ['ideal', 'fault']:
        raise ValueError('mode must be ideal or fault')
    off = mode == 'ideal'
    keys = dict(lift=x.lift_closed_days, E=x.E_closed_days,
        R=x.R_closed_days, port=x.port_closed_days, R0=x.common_fault_days,
        Rc=x.capture_only_fault_days, Rp=x.processor_only_fault_days,
        cargo=x.cargo_lost_batches, hull=x.hull_losses,
        tank=x.tank_loss_incidents, processor_spares=x.spare_processor_modules)
    return {k: 0 if off else int(v) for k, v in keys.items()}


def _component(route, G, eta, x, m, mode, *, flights_per_batch=2, delta=2):
    b = _budgets(x, mode); P = x.period_days; H = x.water_horizon_days
    Rproc = b['R0'] + b['Rp']; Rcap = b['R0'] + b['Rc']
    plant = size_processor(G, eta, Rproc, x.module_t_day, b['processor_spares'], P)
    if route == 'R':
        packed = flights_per_batch*x.R_payload_t
        # Two (or four) preselected sites have the same nominal250-open-date
        # yearly calendar.  No complementary windows are assumed.
        closed = P-x.R_nominal_open_days+flights_per_batch*b['R']
        lower = upper = x.direct_delivery_days
        delta = 1
        actual_flights_per_batch = flights_per_batch
        landing_ratio = x.direct_touchdown_ratio
        operating_sites = flights_per_batch
    elif route == 'E':
        packed = x.E_payload_t
        closed = b['E']
        lower = int(m['outbound_ready_to_touchdown_days_integer_scenario'])
        upper = lower+x.E_jitter_days
        actual_flights_per_batch = 1
        landing_ratio = float(m['landing_mass_per_net_cargo'])
        operating_sites = 0
    else:
        raise ValueError(route)
    if closed >= P:
        return dict(feasible=False, route=route, reason='No positive guaranteed calendar capacity', G_t_day=G)
    rx = receiver_bound(lower, upper, delta, 4, b['port'], P)
    Q = packed*x.packed_water_fraction
    # Site failures may occur on different dates. A paired batch needs every
    # selected site; union closures and whole-batch losses must include each
    # participating site's count budget without assuming common faults.
    cargo_budget=b['cargo']*actual_flights_per_batch if route=='R' else b['cargo']
    cert = certificate(G, eta, Q, delta, rx['Lmax'], plant['K_t_day'],
        P=P, B=closed, R0=b['R0'], Rc=b['Rc'], Rp=b['Rp'], J=cargo_budget,
        tank_events=b['tank'], C=x.tank_capacity_t)
    if not cert['certified']:
        return dict(feasible=False, route=route, G_t_day=G, eta=eta,
            packed_batch_t=packed, delta=delta, closed_budget=closed,
            receiver=rx, certificate=cert, reason=cert['reason'])
    reserve = math.ceil((cert['reserve_t']+.25*G)/500)*500
    # Dedicated reservoirs rather than an unverified clean/raw repurposing rule.
    # The extra raw input day covers the pre-processing peak on the day grid.
    fresh_capacity = reserve+G
    raw_capacity = G*(Rproc+1)
    fresh_cells = math.ceil(fresh_capacity/x.tank_capacity_t)+b['tank']
    raw_cells = math.ceil(raw_capacity/x.tank_capacity_t)+b['tank']
    cells = fresh_cells+raw_cells
    annual_external = ((1-eta)*G*H + eta*G*budget(H, Rcap, P)
        + Q*budget(H, cargo_budget, P) + x.tank_capacity_t*budget(H, b['tank'], P))
    departures = max(0, math.floor(annual_external/Q+1e-10))
    dry = float(m['return_dry_per_net_cargo'])
    loss_fraction = 0. if mode == 'ideal' else x.annual_propellant_loss_fraction
    recurring = 1+(float(m['beta_outbound_per_net_cargo'])-dry-1)/(1-loss_fraction)
    if recurring < 1:
        raise ValueError('Mission has negative recurring propellant requirement')
    if route == 'E':
        if 'return_tail_upper_days' in m:
            tail=int(m['return_tail_upper_days'])
        else:
            # The difference of independently rounded upper bounds is not an
            # upper bound on their difference.  Round the raw difference.
            tail=math.ceil(float(m['return_cycle_unrounded_days_scenario'])
                -float(m['outbound_ready_to_touchdown_days_scenario']))
        if tail<0:raise ValueError('Negative return/inspection tail')
        cycle = rx['Lmax']+tail
        fleet = fleet_bound(cycle, delta, H, b['hull'], P, x.activation_days)
        base, spare = fleet['base_fleet'], fleet['spare_hulls']
        staged_new = departures*packed*recurring
        dry_mass = (base+spare)*dry*packed
        al = 1-b['lift']/P
        if al <= 0:
            raise ValueError('No positive lift availability')
        gross_lift_rate = x.lift_t_year_per_harbour/P*al
        preposition_days = b['lift']/al+x.climber_transit_days+staged_new/gross_lift_rate
    else:
        fleet = None; base = spare = 0; staged_new = dry_mass = 0.
        gross_lift_rate = 0.; preposition_days = 0.
    modules = plant['installed_modules']
    return dict(feasible=True, route=route, mode=mode, eta=eta, G_t_day=G,
        Q=Q, Qnet=Q, Qpacked=packed, packed_batch_t=packed,
        delta=delta, closed_budget=closed, flights_per_batch=actual_flights_per_batch,
        cargo_lost_batches_budget=cargo_budget,
        R_fault_closed_days_per_site=b['R'] if route=='R' else None,
        R_cargo_losses_per_site=b['cargo'] if route=='R' else None,
        operating_R_sites=operating_sites, nominal_R_open_dates=x.R_nominal_open_days if route=='R' else None,
        receiver=rx, certificate=cert, processor=plant, fleet_certificate=fleet,
        reserve_t=reserve, working_water_t=G, initial_lunar_water_t=reserve+G,
        initial_lunar_packed_t=(reserve+G)/x.packed_water_fraction,
        processing_modules=modules, processor_K_t_day=plant['K_t_day'],
        guaranteed_G_t_day=plant['guaranteed_G_t_day'],
        plant_dry_t=modules*x.module_dry_mass_t,
        plant_power_kW=modules*x.module_power_kW,
        fresh_capacity_required_t=fresh_capacity,
        raw_capacity_required_t=raw_capacity,
        fresh_tank_compartments=fresh_cells,
        raw_tank_compartments=raw_cells,
        tank_compartments=cells,
        tank_hardware_t=cells*x.tank_dry_mass_t,
        hardware_lunar_t=modules*x.module_dry_mass_t+cells*x.tank_dry_mass_t,
        annual_external_loss_envelope_t=annual_external,
        annual_full_departures_upper=departures,
        annual_R_flights=departures*actual_flights_per_batch if route=='R' else 0,
        annual_R_packed_t=departures*packed if route=='R' else 0.,
        annual_E_departures=departures if route=='E' else 0,
        annual_E_packed_cargo_t=departures*packed if route=='E' else 0.,
        annual_E_cargo_newlift=staged_new,
        operating_E_fleet=base+spare, operating_E_base_fleet=base,
        operating_E_spare_hulls=spare,
        operating_E_cycle_days=fleet['cycle_days'] if fleet else 0,
        mission_return_tail_upper_days=tail if route=='E' else 0,
        full_E_dry_deployment_t_before_reuse_credit=dry_mass,
        E_dry_mass_per_hull_t=dry*packed if route=='E' else 0.,
        receiver_actual_flight_slots=4*actual_flights_per_batch,
        receiver_touchdown_t_per_open_day=4*packed*landing_ratio,
        receiver_unload_t_per_open_day=4*packed,
        single_touchdown_t=packed*landing_ratio/actual_flights_per_batch,
        annual_propellant_loss_fraction=loss_fraction,
        recurring_new_lift_per_packed_cargo=recurring if route=='E' else None,
        apex_stock_gross_t=staged_new,
        apex_fixed_harbour_lift_rate_t_day=gross_lift_rate,
        apex_stock_preposition_upper_days=preposition_days,
        tank_fault_model='Single union of raw/fresh isolated-compartment incidents; raw loss is eta*raw_t in the recovered-water-equivalent ledger, at mostC. Each reservoir class has its own capacity spare. Repair<=Pdays.',
        source_scope='Conditional designed service calendar and mission interface; not observations or empirical availability.',
        R_vehicle_scope='R vehicles are expended; their manufacture, propellant and operations belong in each launch cost parameter. No reusable R hull pool is assumed.',
        cargo_hull_support_scope='The cargo-loss budget includes every loss before successful delivery, including cargo destroyed with a hull. The permanent-hull budget may also include losses on the empty return. These are not added as two disjoint pre-delivery cargo-loss budgets.',
        E_staging_scope='All one-year new cargo and retained propellant staged at one fixed-capacity harbour before habitation; reusable dry hulls charged separately with explicit reuse credit by integrated model.')


def _aggregate(components, x, m, mode, eta, name, route):
    failed = [c for c in components if not c.get('feasible')]
    if failed:
        return dict(id=name, name=name, operation_route=route, eta=eta,
            mode=mode, feasible=False, reason='At least one independent service-zone certificate fails', components=components)
    def total(key):
        return sum(c[key] for c in components)
    power = total('plant_power_kW')
    stock = total('apex_stock_gross_t')
    fleet_dry = total('full_E_dry_deployment_t_before_reuse_credit')
    reasons = []
    if x.lunar_power_budget_kW is not None and power > x.lunar_power_budget_kW+1e-8:
        reasons.append('Installed processing modules exceed the declared lunar power budget')
    if x.apex_warehouse_capacity_t is not None and stock+fleet_dry > x.apex_warehouse_capacity_t+1e-8:
        reasons.append('Operating apex stock plus full E fleet exceeds the declared apex storage capacity')
    z = dict(id=name, name=name, eta=eta, operation_route=route,
        mode=mode, feasible=not reasons, reason='; '.join(reasons) if reasons else None,
        components=components, reserve_t=total('reserve_t'),
        working_water_t=total('working_water_t'),
        initial_lunar_water_t=total('initial_lunar_water_t'),
        initial_lunar_packed_t=total('initial_lunar_packed_t'),
        processing_modules=total('processing_modules'),
        processor_K_t_day=total('processor_K_t_day'),
        plant_dry_t=total('plant_dry_t'), plant_power_kW=power,
        fresh_tank_compartments=total('fresh_tank_compartments'),
        raw_tank_compartments=total('raw_tank_compartments'),
        tank_compartments=total('tank_compartments'),
        tank_hardware_t=total('tank_hardware_t'), hardware_lunar_t=total('hardware_lunar_t'),
        operating_R_flights=total('annual_R_flights'),
        annual_R_flights=total('annual_R_flights'),
        annual_R_packed_t=total('annual_R_packed_t'),
        operating_R_sites_required=total('operating_R_sites'),
        operating_E_new_lift_t=total('annual_E_cargo_newlift'),
        annual_E_departures=total('annual_E_departures'),
        annual_E_packed_cargo_t=total('annual_E_packed_cargo_t'),
        operating_E_fleet=total('operating_E_fleet'),
        operating_E_base_fleet=total('operating_E_base_fleet'),
        operating_E_spare_hulls=total('operating_E_spare_hulls'),
        full_E_dry_deployment_t_before_reuse_credit=fleet_dry,
        receiver_actual_flight_slots=total('receiver_actual_flight_slots'),
        receiver_touchdown_t_per_open_day=total('receiver_touchdown_t_per_open_day'),
        receiver_unload_t_per_open_day=total('receiver_unload_t_per_open_day'),
        water_receiver_slots=total('receiver_actual_flight_slots'),
        apex_stock_gross_t=stock,
        apex_stock_preposition_upper_days=max(c['apex_stock_preposition_upper_days'] for c in components),
        gross_service_t_day=x.gross_service_t_day,
        water_horizon_days=x.water_horizon_days, input_scenarios=asdict(x),
        independent_zones=(len(components)>1),
        scope='Finite catalogue, sufficient quantity/service certificates. Multi-zone candidates use distinct source reservations, independent inventories and one redundant processor per fault-mode zone; they do not rely on an unproved pooled inventory policy.',
        guarantee_boundary='Domestic/medical service-water scope; agricultural/industrial/cooling water flows require added inputs. Isolation, purification quality, storage aging and module performance are engineering assumptions.',
        hardware_accounting=HARDWARE_ACCOUNTING,
        hardware_service_life_assumption='Water modules, fresh/raw tanks and incremental power hardware are delivered and commissioned in the late prepositioning stage, not assumed functional after centuries of early storage. They are charged OUTSIDE the generic 100 Mt construction target as an independent increment, so the generic target contains no water hardware and nothing is counted twice. At least one year of rated service after commissioning is assumed, not empirically calibrated.')
    return z


def build_water_catalogue(inputs=None, mission=None, mode='fault'):
    """Return all declared candidates, retaining infeasible cases and reasons."""
    x = inputs or WaterInputs(); _validate(x); m = _mission(mission)
    b = _budgets(x, mode); G = x.gross_service_t_day; H = x.water_horizon_days; P=x.period_days
    stock = G*H+x.tank_capacity_t*budget(H, b['tank'], P)
    cells = math.ceil(stock/x.tank_capacity_t)+b['tank']
    out = [dict(id='stock_all', name='stock_all', eta=0., operation_route=None,
        mode=mode, feasible=True, reason=None, components=[],
        reserve_t=stock, working_water_t=0., initial_lunar_water_t=stock,
        initial_lunar_packed_t=stock/x.packed_water_fraction,
        processing_modules=0, processor_K_t_day=0., plant_dry_t=0.,plant_power_kW=0.,
        fresh_tank_compartments=cells, raw_tank_compartments=0, tank_compartments=cells,
        tank_hardware_t=cells*x.tank_dry_mass_t, hardware_lunar_t=cells*x.tank_dry_mass_t,
        operating_R_flights=0,annual_R_flights=0,annual_R_packed_t=0.,
        operating_R_sites_required=0,
        operating_E_new_lift_t=0.,annual_E_departures=0,annual_E_packed_cargo_t=0.,
        operating_E_fleet=0,operating_E_base_fleet=0,operating_E_spare_hulls=0,
        full_E_dry_deployment_t_before_reuse_credit=0.,
        receiver_actual_flight_slots=0, receiver_touchdown_t_per_open_day=0.,
        receiver_unload_t_per_open_day=0., water_receiver_slots=0,
        apex_stock_gross_t=0.,apex_stock_preposition_upper_days=0.,
        gross_service_t_day=G,water_horizon_days=H,input_scenarios=asdict(x),
        independent_zones=False,
        scope='All one-year usable water initially on Moon; at most declared isolatedC loss events. Initial-water transport route is chosen independently by integrated model.',
        hardware_accounting=HARDWARE_ACCOUNTING,
        hardware_service_life_assumption='Storage tanks are delivered and commissioned during late prepositioning, with at least the modeled one-year rated service after commissioning. No centuries-long storage durability is assumed.',
        guarantee_boundary='Quantity only; long-duration water quality, thermal control and isolation require engineering evidence.')]
    for eta in [.94,.98]:
        for nflight in [2,4]:
            cs=[_component('R',G,eta,x,m,mode,flights_per_batch=nflight)]
            out.append(_aggregate(cs,x,m,mode,eta,f'recycle_{eta:.2f}_R_{nflight}flights_daily','R'))
        for nzones in [2,4]:
            cs=[_component('R',G/nzones,eta,x,m,mode,flights_per_batch=1)
                for _ in range(nzones)]
            for i,c in enumerate(cs):c['reserved_R_site_id']=i+1;c['independent_zone_id']=i+1
            out.append(_aggregate(cs,x,m,mode,eta,f'recycle_{eta:.2f}_R_{nzones}independent_zones','R'))
        for delta in [2,3]:
            cs=[_component('E',G,eta,x,m,mode,delta=delta)]
            out.append(_aggregate(cs,x,m,mode,eta,f'recycle_{eta:.2f}_E_every{delta}days','E'))
        cs=[_component('E',G/2,eta,x,m,mode,delta=2),
            _component('R',G/2,eta,x,m,mode,flights_per_batch=1)]
        out.append(_aggregate(cs,x,m,mode,eta,f'recycle_{eta:.2f}_ER_halfzones','ER'))
    return out


def replay_component(component, calendars, delay_mode='max'):
    """Independent physical daily water replay, including raw-tank quantity loss.

    This checks water/queue/capacity arithmetic only.  The integrated model must
    separately reserve vehicles, launch opportunities, lift and terminal mass.
    Tank calendar values:0 no incident,1 fresh-compartment loss,2 raw loss.
    """
    c=component['certificate']; rx=component['receiver']
    if not component.get('feasible') or not c.get('certified'):
        raise ValueError('A certified component is required')
    T=len(calendars['common']); P=c['P']; Q=c['Q']; G=c['G']; eta=c['eta']
    if T>component.get('water_horizon_days',365):
        raise ValueError('Replay exceeds finite-year resource scope')
    limits={'common':c['R0'],'capture':c['Rc'],'processor':c['Rp'],
        'dispatch':c['B'],'port':rx['port_closed_budget'],'cargo':c['J']}
    def legal(a,limit,binary=True):
        if len(a)!=T:return False
        if binary and any(v not in [0,1,False,True] for v in a):return False
        return all(sum(bool(v) for v in a[max(0,t-P+1):t+1])<=limit for t in range(T))
    for key,lim in limits.items():
        if not legal(calendars[key],lim):raise ValueError('Illegal calendar '+key)
    if any(v not in [0,1,2] for v in calendars['tank']) or not legal(calendars['tank'],c['tank_events'],False):
        raise ValueError('Illegal tank incident calendar')
    fractions=calendars.get('capture_fraction',[0.]*T)
    if len(fractions)!=T or any(not 0<=v<=1 for v in fractions):raise ValueError('Invalid capture fractions')
    r=component['reserve_t'];W=r;Y=0.;pending=0.;Hloss=0.;N=0
    raw_events=defaultdict(list);deadlines=defaultdict(list);queue=deque();shipments=[]
    fresh_down=[];raw_down=[];rows=[];maxerr=0.;minW=r;maxraw=0.;maxfresh=0.;maxqueue=0
    cleanloss=rawloss=0.;maxlate=0
    for t in range(T):
        fresh_down=[d for d in fresh_down if d>t];raw_down=[d for d in raw_down if d>t]
        tank=calendars['tank'][t];z=0.;raw_t=0.
        if tank==1:
            z=min(c['C'],W);W-=z;cleanloss+=z;fresh_down.append(t+P)
        elif tank==2:
            raw_t=min(c['C'],Y/eta);z=eta*raw_t;Y-=z;rawloss+=raw_t;raw_down.append(t+P)
        if (component['fresh_tank_compartments']-len(fresh_down))*c['C'] < component['fresh_capacity_required_t']-1e-7:
            raise AssertionError('Fresh compartment capacity after failure')
        if (component['raw_tank_compartments']-len(raw_down))*c['C'] < component['raw_capacity_required_t']-1e-7:
            raise AssertionError('Raw compartment capacity after failure')
        for sid in raw_events.pop(t,[]):queue.append(sid)
        maxqueue=max(maxqueue,len(queue));assert len(queue)<=rx['pre_service_queue_bound_flights']
        received=0.
        for _ in range(min(0 if calendars['port'][t] else rx['receiver_slots'],len(queue))):
            sid=queue.popleft();batch=shipments[sid]
            assert not batch['settled'];batch['settled']=True;pending-=Q;received+=Q
            maxlate=max(maxlate,t-batch['deadline'])
        missing=0.
        for sid in deadlines.pop(t,[]):
            batch=shipments[sid]
            if batch['lost']:
                assert not batch['settled'];batch['settled']=True;pending-=Q;missing+=Q
            else:assert batch['settled']
        capture_fault=calendars['common'][t] or calendars['capture'][t]
        process_fault=calendars['common'][t] or calendars['processor'][t]
        capture=fractions[t] if capture_fault else 1.
        rawpeak=(Y+eta*G*capture)/eta
        assert rawpeak<=component['raw_capacity_required_t']+1e-6
        maxraw=max(maxraw,rawpeak)
        recovered=0. if process_fault else min(Y+eta*G*capture,c['K'])
        Y+=eta*G*capture-recovered
        freshpeak=W+received+recovered;maxfresh=max(maxfresh,freshpeak)
        assert freshpeak<=component['fresh_capacity_required_t']+1e-6
        W=freshpeak-G
        Hloss+=(1-eta)*G+eta*G*(1-capture)+missing+z
        order=int(t%c['delta']==0 and not calendars['dispatch'][t] and W+Y+pending<=r-Q+1e-8)
        if order:
            if delay_mode=='max':lag=rx['upstream_max_days']
            elif delay_mode=='min':lag=rx['upstream_min_days']
            elif delay_mode=='alternating':lag=rx['upstream_min_days'] if N%2 else rx['upstream_max_days']
            else:raise ValueError('Unknown delay mode')
            sid=len(shipments);lost=bool(calendars['cargo'][t])
            shipments.append(dict(dispatch=t,deadline=t+c['Lmax'],lost=lost,settled=False))
            deadlines[t+c['Lmax']].append(sid)
            if not lost:raw_events[t+lag].append(sid)
            pending+=Q;N+=1
        identity=W+Y+pending-(r-Hloss+Q*N);maxerr=max(maxerr,abs(identity));minW=min(minW,W)
        assert W>=-1e-6 and Y>=-1e-6 and Y<=c['Y_bound']+1e-6
        assert maxerr<1e-5 and N<=component['annual_full_departures_upper']
        rows.append(dict(day=t,fresh_t=W,recovered_equivalent_backlog_t=Y,pending_t=pending,
            raw_tank_loss_t=raw_t,fresh_tank_loss_t=z if tank==1 else 0.,
            cumulative_external_loss_equivalent_t=Hloss,dispatch=order,
            cumulative_dispatches=N,identity_error_t=identity))
    return dict(days=T,minimum_fresh_t=minW,maximum_raw_peak_t=maxraw,
        maximum_fresh_peak_t=maxfresh,maximum_pre_service_queue_batches=maxqueue,
        maximum_lateness_days=maxlate,maximum_identity_error_t=maxerr,
        departures=N,clean_tank_loss_t=cleanloss,raw_tank_loss_t=rawloss,rows=rows,
        scope='Generated arithmetic path only; conditional theorem and integrated resource reservations carry the guarantee, not this finite replay.')


def validate_catalogue(inputs=None,mission=None):
    x=inputs or WaterInputs(); checks=[]
    for mode in ['ideal','fault']:
        catalogue=build_water_catalogue(x,mission,mode)
        for option in catalogue:
            if not option.get('feasible') or not option['components']:continue
            for component in option['components']:
                for tank_kind in ([0] if mode=='ideal' else [1,2]):
                    T=x.water_horizon_days
                    a={key:[0]*T for key in ['common','capture','processor','dispatch','port','cargo','tank']}
                    a['capture_fraction']=[0.]*T
                    if mode=='fault':
                        for day in range(50,min(T,57)):a['common'][day]=1;a['capture_fraction'][day]=1.
                        for day in range(57,min(T,60)):a['processor'][day]=1
                        for day in range(60,min(T,63)):a['capture'][day]=1
                        if T>59:a['tank'][59]=tank_kind
                        for day in range(min(T,component['closed_budget'])):a['dispatch'][day]=1
                        for day in range(185,min(T,192)):a['port'][day]=1
                        firstopen=component['closed_budget']
                        firstopen+=(-firstopen)%component['delta']
                        for k in range(component['certificate']['J']):
                            day=firstopen+k*component['delta']
                            if day<T:a['cargo'][day]=1
                    elif component['route']=='R':
                        # Ideal hardware retains its finite nominal calendar.
                        for day in range(min(T,component['closed_budget'])):a['dispatch'][day]=1
                    for delay in ['min','max','alternating']:
                        trace=replay_component(component,a,delay)
                        checks.append(dict(mode=mode,option=option['id'],component_route=component['route'],
                            tank_kind=tank_kind,delay=delay,minimum_fresh_t=trace['minimum_fresh_t'],
                            raw_tank_loss_t=trace['raw_tank_loss_t'],
                            maximum_identity_error_t=trace['maximum_identity_error_t'],
                            departures=trace['departures']))
    return dict(path_count=len(checks),all_path_checks_pass=True,paths=checks,
        interpretation='Targeted generated checks, not observed data or exhaustive future calendars.')


def run():
    x=WaterInputs();m=_mission(None)
    result=dict(version='v9_symmetric_water_catalogue',inputs=asdict(x),
        packed_water_fraction=x.packed_water_fraction,
        ideal=build_water_catalogue(x,m,'ideal'),fault=build_water_catalogue(x,m,'fault'),
        validation=validate_catalogue(x,m))
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/water_v9.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(ideal=len(result['ideal']),fault=len(result['fault']),
        feasible_fault=sum(o['feasible'] for o in result['fault']),
        path_checks=result['validation']['path_count'])))
    return result


if __name__=='__main__':run()
