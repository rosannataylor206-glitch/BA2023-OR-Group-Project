"""Fixed-capacity construction routes with cargo losses and finite hull spares.

The 3 harbours and 10 selected launch sites are fixed in the main baseline.
Processing calendars, receiving assets, trajectory parameters and all future
hardware ratings are declared design scenarios.  Times are sufficient upper
times under those contracts, not forecasts or unconstrained optimal times.

Model identity (added in this revision): this module does NOT formulate or
solve a MILP.  For a declared elevator share the completion time is a
closed-form sufficient upper bound; policies are compared by enumeration in
joint_v9.py.  The bound has the form

    H = ceil((target_per_source + intercept) / slope)
    slope     = rate * (1 - a1) - Q * j / P
    intercept = rate * (a0 + path_latency + 1) + 4 Q + Q j

where rate is the guaranteed source rate (t/day), Q is payload per full job
(t), j is the per-period cargo-loss allowance (jobs), P is the period (days),
a1/a0 are the affine slope/intercept of the spare-hull deployment burden, and
path_latency is the declared transport latency (days).  Every term is produced
by service_parameters(); the rounding reserves are named constants below.
"""
from dataclasses import asdict, dataclass, replace
import math

from reference.water_v8 import budget, receiver_bound

# ---------------------------------------------------------------------------
# Certificate rounding reserves (team derivation, not official problem data).
# These constants only bound worst-case rounding and unlaunched tail stock.
# Their justification is recorded in proofs/construction_v9.md and in the
# report appendix.  They are named so that every opaque number in the
# closed-form bound can be traced and challenged in review or defence.
# ---------------------------------------------------------------------------
SETTLEMENT_ROUNDING_BATCHES = 4   # per-source in-flight / not-yet-settled jobs
UNSETTLED_TAIL_BATCHES = 5        # per-source unlaunched tail jobs after cutoff
UPSTREAM_DRAIN_BATCHES = 6        # drain allowance: tail stock plus one job in transit
INTEGER_DAY_ROUNDING = 1          # integer-day rounding margin for durations


@dataclass(frozen=True)
class ConstructionInputs:
    period_days: int = 365
    harbours: int = 3
    lift_t_year_per_harbour: float = 179000.
    rocket_sites: int = 10
    rocket_flights_per_site_year: int = 250
    E_payload_t: float = 500.
    R_payload_t: float = 125.
    E_delta_days: int = 2
    lift_closed_days: int = 30
    E_closed_days: int = 60
    R_closed_days: int = 60
    port_closed_days: int = 7
    cargo_losses_E_per_harbour_year: int = 1
    cargo_losses_R_per_site_year: int = 1
    hull_losses_E_per_harbour_year: int = 1
    climber_transit_days: int = 30
    E_delivery_jitter_days: int = 19
    direct_delivery_days: int = 30
    direct_touchdown_ratio: float = 1.5
    hull_activation_days: int = 2
    propellant_storage_loss_fraction: float = .05
    lift_kWh_kg: float = 19.215324422302
    warehouse_unit_t: float = 50000.
    warehouse_total_capacity_t: float | None = None
    terminal_slots_per_module: int = 4
    terminal_touchdown_t_year_per_module: float = 1_000_000.
    terminal_unload_t_year_per_module: float = 1_000_000.
    single_pad_rating_t: float = 1000.
    force_engineering_capacity_limits: bool = False


def ideal_inputs(inputs=None):
    """Identical physical capacity, with operational faults removed."""
    x = inputs or ConstructionInputs()
    return replace(x, lift_closed_days=0, E_closed_days=0,
        R_closed_days=0, port_closed_days=0,
        cargo_losses_E_per_harbour_year=0,
        cargo_losses_R_per_site_year=0,
        hull_losses_E_per_harbour_year=0,
        E_delivery_jitter_days=0, propellant_storage_loss_fraction=0.)


def _mission(mission):
    if mission is not None:
        return mission
    try:
        from physics_v9 import chosen_mission
        return chosen_mission()
    except ImportError:
        from reference.physics_v8 import staged_record
        return staged_record()


def _validate(x, m):
    for name in ['period_days', 'harbours', 'rocket_sites',
                 'rocket_flights_per_site_year', 'E_delta_days',
                 'climber_transit_days', 'direct_delivery_days',
                 'terminal_slots_per_module']:
        z = getattr(x, name)
        if isinstance(z, bool) or int(z) != z or z <= 0:
            raise ValueError(name+' must be a positive integer')
    for name in ['lift_closed_days', 'E_closed_days', 'R_closed_days',
                 'port_closed_days', 'cargo_losses_E_per_harbour_year',
                 'cargo_losses_R_per_site_year',
                 'hull_losses_E_per_harbour_year', 'E_delivery_jitter_days',
                 'hull_activation_days']:
        z = getattr(x, name)
        if isinstance(z, bool) or not math.isfinite(z) or int(z) != z or z < 0:
            raise ValueError(name+' must be a nonnegative integer')
    for name in ['lift_closed_days', 'E_closed_days', 'R_closed_days',
                 'port_closed_days', 'cargo_losses_E_per_harbour_year',
                 'cargo_losses_R_per_site_year',
                 'hull_losses_E_per_harbour_year']:
        if getattr(x, name) >= x.period_days:
            raise ValueError(name+' must be less than the period')
    for name in ['lift_t_year_per_harbour', 'E_payload_t', 'R_payload_t',
                 'direct_touchdown_ratio', 'lift_kWh_kg', 'warehouse_unit_t',
                 'terminal_touchdown_t_year_per_module',
                 'terminal_unload_t_year_per_module', 'single_pad_rating_t']:
        z = getattr(x, name)
        if not math.isfinite(z) or z <= 0:
            raise ValueError(name+' must be positive and finite')
    if not 0 <= x.propellant_storage_loss_fraction < 1:
        raise ValueError('Invalid propellant retention scenario')
    if x.rocket_flights_per_site_year > x.period_days:
        raise ValueError('At most one nominal flight per site per day')
    if x.warehouse_total_capacity_t is not None and (
            not math.isfinite(x.warehouse_total_capacity_t) or x.warehouse_total_capacity_t <= 0):
        raise ValueError('Invalid imposed warehouse rating')
    for k in ['beta_outbound_per_net_cargo', 'return_dry_per_net_cargo',
              'landing_mass_per_net_cargo', 'return_cycle_days',
              'outbound_ready_to_touchdown_days_integer_scenario']:
        if k not in m or not math.isfinite(m[k]) or m[k] <= 0:
            raise ValueError('Missing positive mission interface '+k)
    if m['beta_outbound_per_net_cargo'] < 1+m['return_dry_per_net_cargo']:
        raise ValueError('Mission recurring cargo plus propellant must exceed cargo')


def service_parameters(inputs=None, mission=None):
    """Physical-source service contracts; no aggregate capacity multiplier."""
    x = inputs or ConstructionInputs(); m = _mission(mission); _validate(x, m)
    P = x.period_days
    dry = float(m['return_dry_per_net_cargo'])
    g = 1+(m['beta_outbound_per_net_cargo']-dry-1)/(1-x.propellant_storage_loss_fraction)
    a_lift = 1-x.lift_closed_days/P
    a_port = 1-x.port_closed_days/P
    a_E = 1/x.E_delta_days-x.E_closed_days/P
    a_R = x.rocket_flights_per_site_year/P-x.R_closed_days/P
    if min(a_lift, a_port, a_E, a_R) <= 0:
        raise ValueError('A declared stage has no positive guaranteed rate')
    # The extra day embeds discrete right-continuous service in continuous time.
    Tlift = x.lift_closed_days/a_lift+INTEGER_DAY_ROUNDING
    TdispatchE = (1+x.E_closed_days)/a_E+INTEGER_DAY_ROUNDING
    TdispatchR = (1+x.R_closed_days)/a_R+INTEGER_DAY_ROUNDING
    Tport = (1+x.port_closed_days)/a_port+INTEGER_DAY_ROUNDING
    ready = int(m['outbound_ready_to_touchdown_days_integer_scenario'])
    upper = ready+x.E_delivery_jitter_days
    rxE = receiver_bound(ready, upper, x.E_delta_days, 1, x.port_closed_days, P)
    # Two actual flight receiving slots per site make the 1/day arrival upper
    # envelope stable even if all scheduled arrivals bunch against port closures.
    rxR = receiver_bound(x.direct_delivery_days, x.direct_delivery_days, 1, 2,
                         x.port_closed_days, P)
    # Differences of separately rounded upper bounds are NOT upper bounds.
    # The physics interface supplies the return tail rounded independently.
    if 'return_tail_upper_days' in m:
        tail = m['return_tail_upper_days']
    else:
        tail = math.ceil(m['return_cycle_unrounded_days_scenario']-
                         m['outbound_ready_to_touchdown_days_scenario'])
    C = rxE['Lmax']+max(0., tail)
    Fbase = math.ceil((C+x.hull_activation_days)/x.E_delta_days)
    gross_lift = x.lift_t_year_per_harbour/P*a_lift
    rE = min(gross_lift/g, x.E_payload_t*a_E, x.E_payload_t*a_port)
    rR = min(x.R_payload_t*a_R, 2*x.R_payload_t*a_port)
    return dict(period_days=P, recurring_lift_per_payload=g,
        recurring_lift_no_storage_loss=m['beta_outbound_per_net_cargo']-dry,
        return_dry_per_payload=dry, effective_gross_lift_t_day_per_harbour=gross_lift,
        lift_t_year_per_harbour=x.lift_t_year_per_harbour,
        rE_t_day_per_harbour=rE, rR_t_day_per_site=rR,
        nominal_R_capacity_t_year_per_site=x.rocket_flights_per_site_year*x.R_payload_t,
        Tlift_days=Tlift, TdispatchE_days=TdispatchE,
        TdispatchR_days=TdispatchR, Tport_days=Tport,
        E_path_latency_days=Tlift+x.climber_transit_days+TdispatchE+upper+Tport,
        R_path_latency_days=TdispatchR+x.direct_delivery_days+Tport,
        E_ready_lower_days=ready, E_delivery_upper_days=upper,
        receiver_E=rxE, receiver_R=rxR,
        base_hulls_per_harbour=Fbase, E_cycle_with_receiving_days=C,
        E_return_tail_upper_days=tail,
        E_rotation_hold_days=C+x.hull_activation_days,
        E_channels_per_harbour=1,
        scope='3 fixed harbours and10 fixed selected sites by default; calendar throughput and terminal/warehouse ratings remain explicit design assumptions.')


def _route_plan(route, target, x, m, s, available_E_hulls_per_harbour=0):
    E = route == 'E'; P = x.period_days
    n = x.harbours if E else x.rocket_sites
    Q = x.E_payload_t if E else x.R_payload_t
    rate = s['rE_t_day_per_harbour'] if E else s['rR_t_day_per_site']
    Tpath = s['E_path_latency_days'] if E else s['R_path_latency_days']
    j = x.cargo_losses_E_per_harbour_year if E else x.cargo_losses_R_per_site_year
    h = x.hull_losses_E_per_harbour_year if E else 0
    dry_mass = s['return_dry_per_payload']*Q if E else 0.
    base = s['base_hulls_per_harbour'] if E else 0
    available = available_E_hulls_per_harbour if E else 0
    base_deficit = max(0, base-available)
    lift_rate = s['effective_gross_lift_t_day_per_harbour']
    # S=ceil(hH/P+h) is integer and >= b_h(H). Its real-valued upper
    # bound hH/P+h+1 lets us solve a genuinely affine, monotone certificate.
    a1 = dry_mass*h/(P*lift_rate) if E else 0.
    spare_intercept = h+INTEGER_DAY_ROUNDING if h else 0
    needs_deployment = E and (base_deficit > 0 or h > 0)
    a0 = (s['Tlift_days']+x.climber_transit_days+
          dry_mass*(base_deficit+spare_intercept)/lift_rate+
          INTEGER_DAY_ROUNDING) if needs_deployment else 0.
    slope = rate*(1-a1)-Q*j/P
    intercept = (rate*(a0+Tpath+INTEGER_DAY_ROUNDING)
                 +SETTLEMENT_ROUNDING_BATCHES*Q+Q*j)
    if target <= 0:
        return dict(active=False, route=route, target_t=0., physical_sources=0,
                    completion_upper_days=0, ready_after_flush_days=0,
                    attempts_per_source=0, attempts_total=0, full_payload_t=0.,
                    guarantee_t=0., new_lift_mass_t=0., initial_hull_mass_t=0.,
                    hulls_installed=0, base_hulls_total=0, spare_hulls_total=0,
                    cargo_lost_t_upper=0., hull_losses_total_upper=0,
                    warehouse_required_t=0., warehouse_packages=0,
                    warehouse_required_per_harbour_t=[], landing_t_upper=0.,
                    lift_energy_kWh_upper=0., terminal_slots_reserved=0,
                    terminal_touchdown_t_open_day=0., terminal_unload_t_open_day=0.,
                    retained_upstream_full_payload_t_upper=0.,
                    quarantine_apex_gross_t_upper=0.,
                    quarantine_ground_payload_t_upper=0.,
                    guaranteed_intact_base_after_handoff=available*n,
                    base_hulls_per_harbour_after_handoff=available)
    if slope <= 0:
        return dict(active=True, route=route, target_t=target, feasible=False,
            reason='Selected fixed capacity cannot sustain this affine replacement/loss guarantee',
            affine_net_rate_t_day_per_source=slope)
    per_target = target/n
    H = max(1, math.ceil((per_target+intercept)/slope))
    # Compute all policy quantities from integer H; their exact certificate
    # must dominate the affine bound used to choose H.
    spare = math.ceil(h*H/P+h-1e-12) if h else 0
    fleet_new = base_deficit+spare
    fleet_present = max(base, available)+spare
    deployment = math.ceil(s['Tlift_days']+x.climber_transit_days+
                          dry_mass*fleet_new/lift_rate) if needs_deployment else 0
    source_days = math.floor(H-deployment-Tpath)
    source_mass = rate*source_days
    attempts = math.ceil(source_mass/Q-1e-12)
    exact_loss = int(budget(H, j, P))
    exact_hull_loss = int(budget(H, h, P))
    settled_attempts_mass_lower = max(0., source_mass-SETTLEMENT_ROUNDING_BATCHES*Q)
    guar_per = settled_attempts_mass_lower-Q*exact_loss
    affine_lower = slope*H-intercept
    if (source_days < 0 or guar_per < per_target-1e-6 or
            guar_per < affine_lower-1e-6 or spare < exact_hull_loss or
            attempts*Q < source_mass-1e-7 or attempts*Q-source_mass > Q+1e-7):
        raise AssertionError('Construction certificate failed independent arithmetic guards')
    # Actual departures stop at H. Upstream residual is quarantined, never
    # launched during the handoff tail; all loss dates are therefore <= H.
    # Drain only pre-H in-flight cargo and the remaining lift-to-apex stream.
    # Source surplus has at most five full jobs per source. Its full cost
    # is charged although some allocated jobs may remain unlaunched.
    upstream_wait = (s['Tlift_days']+x.climber_transit_days
                     +UPSTREAM_DRAIN_BATCHES*Q/rate) if E else 0.
    in_flight_wait = s['receiver_E']['Lmax'] if E else s['receiver_R']['Lmax']
    return_wait = s['E_return_tail_upper_days']+x.hull_activation_days if E else 0.
    flush = max(upstream_wait, in_flight_wait+return_wait)
    initial_hull_mass = n*fleet_new*dry_mass
    payload_mass = n*attempts*Q
    new_lift = s['recurring_lift_per_payload']*payload_mass+initial_hull_mass if E else 0.
    # A source regulator gives a finite apex burst; terminal cargo queues are
    # separately bounded by receiver_E and not counted as apex storage.
    per_hub_store = (s['recurring_lift_per_payload']*max(
        rate*(s['Tlift_days']+s['TdispatchE_days'])+2*Q,UNSETTLED_TAIL_BATCHES*Q)
        +fleet_present*dry_mass) if E else 0.
    wh_units = math.ceil(per_hub_store/x.warehouse_unit_t-1e-12) if E else 0
    land_ratio = m['landing_mass_per_net_cargo'] if E else x.direct_touchdown_ratio
    slot_per = 1 if E else 2
    return dict(active=True, feasible=True, route=route, target_t=target,
        physical_sources=n, completion_upper_days=H,
        completion_upper_years=H/P, ready_after_flush_days=H+flush,
        initial_deployment_days=deployment, source_duration_days=source_days,
        source_rate_t_day_per_source=rate, source_input_t_per_source=source_mass,
        attempts_per_source=attempts, attempts_total=n*attempts,
        full_payload_t=payload_mass, guarantee_t=n*guar_per,
        guarantee_per_source_t=guar_per,
        settled_attempts_mass_lower_per_source_t=settled_attempts_mass_lower,
        cargo_loss_count_per_source_upper=exact_loss,
        cargo_lost_t_upper=n*Q*exact_loss,
        cargo_loss_affine_count_per_source=j*H/P+j,
        affine_net_rate_t_day_per_source=slope,
        affine_intercept_t_per_source=intercept,
        affine_lower_delivered_per_source_t=affine_lower,
        deployment_affine_days_intercept=a0,
        deployment_affine_days_slope=a1,
        base_hulls_per_harbour=base, spare_hulls_per_harbour=spare,
        hull_loss_count_per_harbour_upper=exact_hull_loss,
        hull_losses_total_upper=n*exact_hull_loss,
        hulls_installed=n*fleet_new, hulls_present_after_deployment=n*fleet_present,
        available_intact_hulls_per_harbour=available,
        new_base_hulls_per_harbour=base_deficit,
        base_hulls_total=n*base,
        spare_hulls_total=n*spare,
        guaranteed_intact_base_after_handoff=n*max(base, available),
        base_hulls_per_harbour_after_handoff=max(base, available),
        unused_spares_not_credited_to_next_phase=True,
        initial_hull_mass_t=initial_hull_mass, new_lift_mass_t=new_lift,
        warehouse_required_t=n*per_hub_store,
        warehouse_required_per_harbour_t=[per_hub_store]*n if E else [],
        warehouse_packages=n*wh_units,
        warehouse_installed_capacity_t=n*wh_units*x.warehouse_unit_t,
        terminal_slots_reserved=n*slot_per,
        terminal_touchdown_t_open_day=n*slot_per*Q*land_ratio,
        terminal_unload_t_open_day=n*slot_per*Q,
        landing_t_upper=payload_mass*land_ratio,
        lift_energy_kWh_upper=new_lift*1000*x.lift_kWh_kg,
        queue_flush_upper_days=flush, final_return_wait_days=return_wait,
        actual_dispatch_cutoff_days=H,
        no_dispatches_during_handoff=True,
        attempt_count_kind='Full allocated source jobs; conservative upper count of actual attempts. Unlaunched tail inventory is retained and receives no next-phase credit.',
        retained_upstream_full_payload_t_upper=n*UNSETTLED_TAIL_BATCHES*Q,
        quarantine_apex_gross_t_upper=n*UNSETTLED_TAIL_BATCHES*Q*s['recurring_lift_per_payload'] if E else 0.,
        quarantine_ground_payload_t_upper=n*UNSETTLED_TAIL_BATCHES*Q if not E else 0.,
        unsettled_job_count_per_source_upper=UNSETTLED_TAIL_BATCHES,
        fullpacket_source_overrun_per_source_t=attempts*Q-source_mass,
        proof_scope='Affine sufficient completion certificate. Full charge for every attempt, including destroyed cargo. Permanent E hulls and ready replacements are predeployed before the cargo source begins.')


def plan_construction(elevator_share, inputs=None, mission=None, target_t=100_000_000.,
                      available_E_hulls_per_harbour=0):
    """Construct a sufficient fixed-capacity plan for a declared cargo split.

    This returns one feasible policy certificate, not the globally fastest or
    cheapest arbitrary schedule. Root orchestration compares a finite share
    catalogue and reports that catalogue honestly.
    """
    if (not math.isfinite(elevator_share) or not 0 <= elevator_share <= 1 or
            not math.isfinite(target_t) or target_t < 0):
        raise ValueError('A finite split in[0,1] and nonnegative target required')
    if (isinstance(available_E_hulls_per_harbour, bool) or
            int(available_E_hulls_per_harbour) != available_E_hulls_per_harbour or
            available_E_hulls_per_harbour < 0):
        raise ValueError('Available hulls must be a nonnegative integer per harbour')
    x = inputs or ConstructionInputs(); m = _mission(mission)
    s = service_parameters(x, m)
    E = _route_plan('E', target_t*elevator_share, x, m, s,
                    available_E_hulls_per_harbour)
    R = _route_plan('R', target_t*(1-elevator_share), x, m, s)
    if not E.get('feasible', True) or not R.get('feasible', True):
        return dict(feasible=False, inputs=asdict(x), elevator_share=elevator_share,
                    routes={'E': E, 'R': R}, service=s)
    slots = E['terminal_slots_reserved']+R['terminal_slots_reserved']
    touch = E['terminal_touchdown_t_open_day']+R['terminal_touchdown_t_open_day']
    unload = E['terminal_unload_t_open_day']+R['terminal_unload_t_open_day']
    term = max(math.ceil(slots/x.terminal_slots_per_module),
        math.ceil(touch/(x.terminal_touchdown_t_year_per_module/x.period_days)),
        math.ceil(unload/(x.terminal_unload_t_year_per_module/x.period_days)))
    pad_required = max(x.E_payload_t*m['landing_mass_per_net_cargo'] if E['active'] else 0.,
                       x.R_payload_t*x.direct_touchdown_ratio if R['active'] else 0.)
    wh = E['warehouse_required_t']
    capacity_checks = dict(
        payload_guarantee=E['guarantee_t']+R['guarantee_t'] >= target_t-1e-6,
        fixed_harbours=x.harbours == 3,
        fixed_rocket_sites=x.rocket_sites == 10,
        no_lift_capacity_multiplier=True,
        terminal_slots=slots <= term*x.terminal_slots_per_module,
        terminal_touchdown=touch <= term*x.terminal_touchdown_t_year_per_module/x.period_days+1e-7,
        terminal_unload=unload <= term*x.terminal_unload_t_year_per_module/x.period_days+1e-7,
        single_pad_rating=pad_required <= x.single_pad_rating_t,
        imposed_warehouse=(x.warehouse_total_capacity_t is None or wh <= x.warehouse_total_capacity_t+1e-7))
    feasible = (capacity_checks['payload_guarantee'] and
                (not x.force_engineering_capacity_limits or
                 capacity_checks['single_pad_rating'] and capacity_checks['imposed_warehouse']))
    H = max(E['completion_upper_days'], R['completion_upper_days'])
    ready = max(E['ready_after_flush_days'], R['ready_after_flush_days'])
    features = dict(E_lift_t=E['new_lift_mass_t'], R_launches=R['attempts_total'],
        E_mission_attempts=E['attempts_total'], E_hulls=E['hulls_installed'],
        E_dry_hardware_t=E['initial_hull_mass_t'],
        warehouse_packages=E['warehouse_packages'], terminal_modules=term,
        lift_energy_kWh=E['lift_energy_kWh_upper'],
        rocket_payload_t=R['full_payload_t'],
        cargo_lost_t_upper=E['cargo_lost_t_upper']+R['cargo_lost_t_upper'],
        hulls_lost_upper=E['hull_losses_total_upper'],
        source_lunar_payload_t=E['full_payload_t']+R['full_payload_t'],
        elapsed_days=H, harbours_used=x.harbours if E['active'] else 0,
        rocket_sites_used=x.rocket_sites if R['active'] else 0)
    return dict(version='v9_fixed_capacity_construction', feasible=bool(feasible),
        elevator_share=elevator_share, target_t=target_t,
        construction_completion_upper_days=H,
        construction_completion_upper_years=H/x.period_days,
        constructioncompletionupperdays=H,
        ready_for_water_days=ready, handoff_additional_upper_days=ready-H,
        guaranteed_delivered_t=E['guarantee_t']+R['guarantee_t'],
        routes={'E': E, 'R': R}, service=s, inputs=asdict(x), features=features,
        resource_checks=capacity_checks,
        warehouse_required_t=wh, warehouse_packages=E['warehouse_packages'],
        warehouse_capacity_scope='Per-harbour integer procurement output. Optional explicit capacity stress is separate from the original fixed-lift baseline.',
        terminal_modules=term, terminal_reserved_flights_per_open_day=slots,
        terminal_touchdown_required_t_open_day=touch,
        terminal_unload_required_t_open_day=unload,
        single_pad_required_t=pad_required,
        single_pad_installed_rating_t=max(pad_required, x.single_pad_rating_t) if not x.force_engineering_capacity_limits else x.single_pad_rating_t,
        initial_E_hulls=E['hulls_installed'],
        base_E_hulls_after_handoff=E['guaranteed_intact_base_after_handoff'],
        base_E_hulls_per_harbour_after_handoff=E['base_hulls_per_harbour_after_handoff'],
        quarantined_E_apex_gross_t_upper=E['quarantine_apex_gross_t_upper'],
        quarantined_R_ground_payload_t_upper=R['quarantine_ground_payload_t_upper'],
        unused_construction_spares_not_reused=True,
        capacity_identity='Official3harbours×179000gross tonnes/year and selected10sites fixed;250flights/site/year, receiver and warehouse capacities are scenario/design inputs, not supplied future empirical data.',
        scope='Sufficient calendar, mass-loss, fleet and phase certificate for this explicit policy and fixed capacities. Time is a conservative upper bound, not an earliest opening date or a future technology forecast.')


if __name__ == '__main__':
    import json
    rows=[]
    for mode, x in [('ideal', ideal_inputs()), ('fault', ConstructionInputs())]:
        for share in [0., .5, 1.]:
            p = plan_construction(share, x)
            rows.append(dict(mode=mode, share=share, feasible=p['feasible'],
                years=p.get('construction_completion_upper_years'),
                delivered=p.get('guaranteed_delivered_t'), features=p.get('features')))
    print(json.dumps(rows, ensure_ascii=False, indent=2))
