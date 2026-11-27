"""Independent water faults, intermittent receiving, and finite-horizon hull spares.

All numerical fault limits are declared engineering scenarios.  This module
does not estimate lunar failure probabilities or real plant mass/power.
"""
from pathlib import Path
from collections import defaultdict, deque
import csv
import itertools
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent


def _integer(x, name, minimum=0):
    if isinstance(x, (bool, np.bool_)) or not math.isfinite(float(x)) or int(x) != x or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(x)


def budget(n, b, P=365):
    """Count envelope for <=1 event/day, at most b events in every P days."""
    P = _integer(P, 'P', 1); b = _integer(b, 'budget')
    if b > P:
        raise ValueError('A binary-day budget cannot exceed the period')
    n = np.asarray(n)
    if np.any(~np.isfinite(n)) or np.any(n < 0) or np.any(n != np.floor(n)):
        raise ValueError('Nonnegative integer interval lengths required')
    n = n.astype(np.int64)
    ans = b * (n // P) + np.minimum(b, n % P)
    return int(ans) if ans.ndim == 0 else ans


def certificate(G, eta, Q, delta, Lmax, K, P=365, B=60, R0=7,
                Rc=3, Rp=3, J=1, tank_events=1, C=1000., review=1):
    """A conservative sufficient reserve for separate capture/processor faults.

    G includes only the declared service-water scope. Q is net usable water.
    R0 common days, Rc capture-only days, Rp processor-only days are each
    separate rolling budgets.  Arbitrary overlaps/correlation are permitted.
    """
    P = _integer(P, 'P', 1)
    vals = [delta, Lmax, B, R0, Rc, Rp, J, tank_events, review]
    delta, Lmax, B, R0, Rc, Rp, J, tank_events, review = [
        _integer(x, name, 1 if name in ['delta', 'Lmax', 'review'] else 0)
        for x, name in zip(vals, ['delta', 'Lmax', 'B', 'R0', 'Rc', 'Rp', 'J', 'tank_events', 'review'])]
    if not all(math.isfinite(float(x)) for x in [G, eta, Q, K, C]):
        raise ValueError('Finite physical quantities required')
    if not (G > 0 and 0 < eta <= 1 and Q > 0 and K > 0 and C >= 0):
        raise ValueError('Invalid physical quantities')
    Rcap, Rproc = R0 + Rc, R0 + Rp
    if not (B < P and Rcap <= P and Rproc < P and J <= P and tank_events <= P):
        raise ValueError('Unsupported event budgets')
    D = (1 - eta) * G
    a = 1 / delta - B / P
    margin = Q * a - D - eta * G * Rcap / P - Q * J / P - C * tank_events / P
    process_margin = K * (1 - Rproc / P) - eta * G
    valid = a > 0 and margin > 1e-9 and process_margin >= -1e-9 and K >= eta * G - 1e-9
    out = dict(certified=bool(valid), G=G, eta=eta, Q=Q, delta=delta,
               Lmax=Lmax, K=K, P=P, B=B, R0=R0, Rc=Rc, Rp=Rp, J=J,
               tank_events=tank_events, C=C, capture_union_budget=Rcap,
               processing_union_budget=Rproc, Y_bound=eta * G * Rproc,
               raw_volume_bound_t=G * Rproc,
               transport_margin_t_day=margin, processing_margin_t_day=process_margin,
               scope='Sufficient daily-quantity guarantee, independent capture/processor calendars; arbitrary correlations within declared rolling supports. Not exact minimum reserve or a shortage probability.')
    if not valid:
        out['reason'] = 'Declared sufficient rate conditions fail; this is not an all-policy infeasibility proof.'
        return out
    E = Lmax + review - 1
    n0 = math.ceil((1 + B) / a)
    H = math.lcm(P, delta)
    switch = P * math.ceil(Rproc / Rp) if Rp > 0 else P
    periodic_start = max(E + n0, switch)
    n = np.arange(E, periodic_start + H + 1, dtype=np.int64)
    # Both are independently valid. The partition bound recovers the original
    # common-fault cancellation, without incorrectly imposing common timing on
    # capture-only and processor-only events.
    separate = eta * G * (budget(n, Rcap, P) + Rproc)
    partition = eta * G * np.maximum(Rproc, budget(n, R0, P) + budget(n, Rc, P) + budget(n, Rp, P))
    water_envelope = np.minimum(separate, partition)
    A = D * n + water_envelope + Q * budget(n, J, P) + C * budget(n, tank_events, P)
    k = n - E
    S = Q * np.maximum(0, k // delta - budget(k, B, P))
    i = int(np.argmax(A - S))
    reserve = Q + float((A - S)[i])
    loose_A = D * n + separate + Q * budget(n, J, P) + C * budget(n, tank_events, P)
    separate_reserve = Q + float(np.max(loose_A - S))
    out.update(reserve_t=reserve, required_reserve_t=reserve,
               critical_interval_days=int(n[i]), finite_scan_end_days=int(n[-1]),
               periodic_descent_t=H * margin, review_days=review,
               envelope_mode='min_of_separate_and_partitioned_suffix_bounds',
               envelope_switch_days=switch, periodic_start_days=periodic_start,
               separate_reserve_t=separate_reserve,
               tightening_vs_separate_t=separate_reserve - reserve,
               conservatism='Minimum of two independently proved safe loss/backlog envelopes; separate calendar budgets remain explicit. Sufficient reserve, not a minimum-reserve theorem.')
    return out


def receiver_bound(lower, upper, delta, slots, port_closed_budget=7, P=365):
    """FIFO completed-delivery bound including complete port closure days.

    The queue starts empty, arrival precedes service, service is work conserving
    on open days, and at most one dispatched batch occurs every delta days.
    """
    lower, upper, delta, slots, B, P = [
        _integer(x, n, 0 if n == 'port_closed_budget' else 1)
        for x, n in zip([lower, upper, delta, slots, port_closed_budget, P],
                        ['lower', 'upper', 'delta', 'slots', 'port_closed_budget', 'P'])]
    if lower > upper or B >= P:
        raise ValueError('Invalid arrival bounds or port budget')
    slack = slots * (1 - B / P) - 1 / delta
    if slack <= 1e-12:
        raise ValueError('This receiver certificate requires strict long-run service slack')
    H = math.lcm(P, delta)
    n = np.arange(1, H + 1, dtype=np.int64)
    alpha = (n + upper - lower + delta - 1) // delta
    served_before_today = slots * ((n - 1) - budget(n - 1, B, P))
    queue = int(np.max(alpha - served_before_today))
    # The count of guaranteed open dates is nondecreasing. This finite upper
    # bracket follows by collecting whole periods of P-B open dates.
    h_upper = P * math.ceil(queue / (slots * (P - B)))
    h = next(k for k in range(1, h_upper + 1) if slots * (k - budget(k, B, P)) >= queue)
    return dict(upstream_min_days=lower, upstream_max_days=upper, delta=delta,
                receiver_slots=slots, port_closed_budget=B, P=P,
                pre_service_queue_bound_flights=queue, processing_dates_bound=h,
                queue_wait_days_bound=h - 1, Lmax=upper + h - 1,
                Lmax_days=upper + h - 1, finite_queue_scan_days=H,
                receiver_rate_slack_flights_day=slack,
                queue_period_descent_flights=H * slack,
                scope='Empty initial FIFO queue; complete port outages allowed within rolling budget; work-conserving open-day receiving. Conservative queue plus service bound, not exact worst delay.')


def size_processor(Gmax, eta, Rproc, module_t_day=25., spare_modules=1, P=365):
    """Modules survive simultaneous spare_modules off line plus fault days."""
    P = _integer(P, 'P', 1); Rproc = _integer(Rproc, 'Rproc')
    spare_modules = _integer(spare_modules, 'spare_modules')
    if (not all(math.isfinite(float(x)) for x in [Gmax, eta, module_t_day]) or
            not (0 <= Rproc < P and Gmax > 0 and 0 < eta <= 1 and module_t_day > 0)):
        raise ValueError('Invalid plant design quantities')
    need = eta * Gmax * P / (P - Rproc)
    active = math.ceil(need / module_t_day - 1e-12)
    K = active * module_t_day
    return dict(installed_modules=active + spare_modules,
                online_modules_after_module_loss=active, spare_modules=spare_modules,
                module_t_day=module_t_day, K_t_day=K,
                nameplate_t_day=(active + spare_modules) * module_t_day,
                required_K_t_day=need, Gmax=Gmax, eta=eta, Rproc=Rproc, P=P,
                processing_margin_t_day=K * (1 - Rproc / P) - eta * Gmax,
                guaranteed_G_t_day=K * (1 - Rproc / P) / eta,
                module_mass_t=None, module_power_kW=None,
                scope='Capacity modules are design units; mass, power, cost and water quality require separately stated engineering inputs. K is after the declared number of modules is unavailable.')


def fleet_bound(cycle_days, delta=1, horizon_days=365, losses_per_period=1,
                P=365, activation_days=2):
    """Finite-horizon permanent-hull-loss guarantee with prepositioned spares.

    Each dispatched hull returns or is confirmed permanently lost within
    cycle_days. A ready spare can replace the lost hull within activation_days.
    Loss support is indexed by dispatch date, <=1 loss per dispatch/day.
    """
    cycle_days, delta, horizon_days, loss, P, activation = [
        _integer(x, n, 0 if n in ['losses_per_period', 'activation_days'] else 1)
        for x, n in zip([cycle_days, delta, horizon_days, losses_per_period, P, activation_days],
                        ['cycle_days', 'delta', 'horizon_days', 'losses_per_period', 'P', 'activation_days'])]
    if loss > P:
        raise ValueError('Hull loss budget exceeds binary-day period')
    base = math.ceil((cycle_days + activation) / delta)
    spares = budget(horizon_days, loss, P)
    return dict(base_fleet=base, spare_hulls=spares, total_hulls=base + spares,
                cycle_days=cycle_days, activation_days=activation,
                rotation_hold_days=cycle_days + activation, delta=delta,
                horizon_days=horizon_days, losses_per_period=loss, P=P,
                scope='Finite dispatch horizon only; spare hulls are initially at the dispatch side, not automatically lunar-landed mass. Each loss is recognized within cycle_days. No unlimited-lifetime guarantee with finite hull stock.')


def _support(flags, P, b):
    a = np.asarray(flags)
    if a.ndim != 1 or np.any((a != 0) & (a != 1)):
        return False
    s = np.r_[0, np.cumsum(a.astype(int))]
    end = np.arange(1, len(a) + 1)
    return bool(np.all(s[end] - s[np.maximum(0, end - P)] <= b))


def replay(design, calendars, delay_mode='alternating', save_rows=False):
    """Physical W/Y/P events, open-day FIFO service, finite spare-hull rotation."""
    c = design['certificate']; rx = design['receiver']; fl = design['fleet']
    P = c['P']; T = len(calendars['common'])
    if not c.get('certified', False) or design['reserve_t'] < c['reserve_t'] - 1e-8:
        raise ValueError('Replay requires a certified design and at least its sufficient reserve')
    if rx['delta'] != c['delta'] or rx['P'] != P:
        raise ValueError('Receiver calendar does not match the water certificate')
    if fl['delta'] != c['delta'] or fl['P'] != P:
        raise ValueError('Fleet calendar does not match the water certificate')
    if (fl['rotation_hold_days'] < fl['cycle_days'] + fl['activation_days'] or
            fl['base_fleet'] * fl['delta'] < fl['rotation_hold_days']):
        raise ValueError('Fleet rotation cannot cover the cycle and activation contract')
    if fl['spare_hulls'] < budget(fl['horizon_days'], fl['losses_per_period'], P):
        raise ValueError('Fleet descriptor understates its finite-horizon spare requirement')
    budgets = dict(common=c['R0'], capture=c['Rc'], processor=c['Rp'],
                   dispatch=c['B'], port=rx['port_closed_budget'], cargo=c['J'],
                   tank=c['tank_events'], hull=fl['losses_per_period'])
    for name, limit in budgets.items():
        if len(calendars[name]) != T or not _support(calendars[name], P, limit):
            raise ValueError('Calendar outside declared support: ' + name)
    capture_fraction = np.asarray(calendars.get('capture_fraction', np.zeros(T)), dtype=float)
    if (len(capture_fraction) != T or np.any(~np.isfinite(capture_fraction)) or
            np.any(capture_fraction < 0) or np.any(capture_fraction > 1)):
        raise ValueError('Fault-day capture fractions must be finite values in [0,1]')
    if T > fl['horizon_days']:
        raise ValueError('Fleet horizon does not cover simulation')
    G, eta, Q, K, delta, L = (c[k] for k in ['G', 'eta', 'Q', 'K', 'delta', 'Lmax'])
    lower, upper = rx['upstream_min_days'], rx['upstream_max_days']
    if L < rx['Lmax']:
        raise ValueError('Water deadline shorter than the proven receiving bound')
    if fl['cycle_days'] < L:
        raise ValueError('Cycle shorter than completed delivery')
    r = design['reserve_t']; W = r; Y = 0.; pending = 0.; Hloss = 0.; departures = 0
    raw_events = defaultdict(list); deadlines = defaultdict(list); hull_events = defaultdict(list)
    queue = deque(); shipments = []; ready = np.zeros(fl['base_fleet'], dtype=int)
    spare_used = 0; spare_committed = 0; minW = r; maxW = r; maxY = 0.; maxqueue = 0; err = 0.; rows = []
    maxlate = 0; tankloss_total = 0.; cargo_total = 0.; captures_total = 0.
    C = c['C']; tank_repairs = []
    Nc = math.ceil((r + G) / C) + c['tank_events'] if C > 0 else None
    for t in range(T):
        tank_repairs = [x for x in tank_repairs if x > t]
        if calendars['tank'][t] and C > 0:
            tank_repairs.append(t + P)
        if C > 0:
            assert (Nc - len(tank_repairs)) * C >= r + G - 1e-8
        z = min(C, max(0., W)) if calendars['tank'][t] else 0.
        W -= z; tankloss_total += z
        for slot in hull_events.pop(t, []):
            spare_used += 1
            if spare_used > fl['spare_hulls']:
                raise AssertionError('Prepositioned spare pool exhausted')
            ready[slot] = max(ready[slot], t + fl['activation_days'])
        for sid in raw_events.pop(t, []):
            queue.append(sid)
        maxqueue = max(maxqueue, len(queue))
        assert len(queue) <= rx['pre_service_queue_bound_flights']
        received = 0.
        slots = 0 if calendars['port'][t] else rx['receiver_slots']
        for _ in range(min(slots, len(queue))):
            sid = queue.popleft(); batch = shipments[sid]
            if batch['settled']:
                raise AssertionError('Duplicate or late delivery')
            batch['settled'] = True; batch['delivery'] = t
            pending -= Q; received += Q
            maxlate = max(maxlate, t - batch['deadline'])
        missing = 0.
        for sid in deadlines.pop(t, []):
            batch = shipments[sid]
            if batch['lost']:
                assert not batch['settled']
                batch['settled'] = True; pending -= Q; missing += Q
            elif not batch['settled']:
                raise AssertionError('Successful batch exceeded deadline')
        collect_fault = calendars['common'][t] or calendars['capture'][t]
        process_fault = calendars['common'][t] or calendars['processor'][t]
        capture = float(capture_fraction[t]) if collect_fault else 1.
        recovered = 0. if process_fault else min(Y + eta * G * capture, K)
        Y += eta * G * capture - recovered
        peak = W + received + recovered
        W = peak - G
        h = (1 - eta) * G + eta * G * (1 - capture) + missing + z
        Hloss += h; cargo_total += missing; captures_total += eta * G * (1 - capture)
        order = int(t % delta == 0 and not calendars['dispatch'][t] and W + Y + pending <= r - Q + 1e-8)
        if order:
            slot = (t // delta) % fl['base_fleet']
            if ready[slot] > t:
                raise AssertionError('Fleet rotation cannot supply promised opportunity')
            ready[slot] = t + fl['rotation_hold_days']
            sid = len(shipments); lost = bool(calendars['cargo'][t])
            if delay_mode == 'min': lag = lower
            elif delay_mode == 'max': lag = upper
            elif delay_mode == 'alternating': lag = lower if sid % 2 else upper
            elif delay_mode == 'bunch': lag = max(lower, min(upper, upper - t % (upper - lower + 1)))
            else: raise ValueError('Unknown deterministic delay pattern')
            batch = dict(dispatch=t, deadline=t + L, lost=lost, settled=False)
            shipments.append(batch); deadlines[t + L].append(sid)
            if not lost: raw_events[t + lag].append(sid)
            if calendars['hull'][t]:
                hull_events[t + fl['cycle_days']].append(slot)
                spare_committed += 1
                if spare_committed > fl['spare_hulls']:
                    raise AssertionError('Spare stock cannot cover losses on all dispatched trips, including tail')
            pending += Q; departures += 1
        identity = W + Y + pending - (r - Hloss + Q * departures)
        err = max(err, abs(identity)); minW = min(minW, W); maxW = max(maxW, W); maxY = max(maxY, Y)
        assert W >= -1e-6 and W <= r + 1e-6 and Y <= c['Y_bound'] + 1e-6
        assert peak <= r + G + 1e-6 and err < 1e-5
        if save_rows:
            rows.append(dict(day=t, fresh_t=W, recoverable_t=Y, pending_t=pending,
                             arrivals_t=received, recovered_t=recovered, gross_use_t=G,
                             tank_loss_t=z, capture_loss_t=eta * G * (1 - capture),
                             deadline_cargo_loss_t=missing, dispatch=order,
                             common=int(calendars['common'][t]), capture_fault=int(calendars['capture'][t]),
                             processor_fault=int(calendars['processor'][t]), port_closed=int(calendars['port'][t]),
                             preconsumption_peak_t=peak, cumulative_departures=departures,
                             cumulative_external_loss_t=Hloss, spare_hulls_used=spare_used,
                             inventory_identity_error_t=identity))
    tail = sum(len(v) for v in hull_events.values())
    assert spare_used + tail == spare_committed <= fl['spare_hulls']
    return dict(days=T, minimum_fresh_t=minW, maximum_fresh_t=maxW, maximum_Y_t=maxY,
                maximum_receiver_queue=maxqueue, maximum_lateness_days=maxlate,
                maximum_identity_error_t=err, departures=departures,
                spare_hulls_used=spare_used, permanent_hull_losses_on_dispatched_trips=spare_committed,
                tail_hull_replacements=tail, spare_pool_tail_commitments_covered=True,
                tank_loss_t=tankloss_total,
                capture_loss_t=captures_total, cargo_loss_t=cargo_total), rows


def _write_csv(path, rows):
    if not rows: return
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def _periodic(T, P, day, count=1):
    t = np.arange(T)
    return np.zeros(T, dtype=bool) if day is None else ((t - day) % P) < count


def run():
    outdir = ROOT / 'results'; outdir.mkdir(exist_ok=True)
    designs = []
    for eta in [.94, .98]:
        for gf in [1., 1.1, 1.2]:
            g = 962 * gf
            plant = size_processor(g, eta, 10)
            rx = receiver_bound(30, 60, 1, 4, 7)
            cert = certificate(g, eta, 103.618, 1, rx['Lmax'], plant['K_t_day'])
            reserve = math.ceil((cert['reserve_t'] + .25 * g) / 500) * 500 if cert['certified'] else None
            fleet = fleet_bound(rx['Lmax'] + 30)
            designs.append(dict(eta=eta, G_factor=gf, plant=plant, receiver=rx, certificate=cert,
                                reserve_t=reserve, fleet=fleet))
    representative = next(d for d in designs if d['eta'] == .98 and d['G_factor'] == 1.2)
    # Retain the tighter original theorem on its original shared-only support;
    # the broader theorem deliberately forgoes its common-loss cancellation.
    from legacy_v7.water_v7 import certificate as shared_certificate
    shared_comparison = []
    for eta in [.94, .98]:
        K = size_processor(962., eta, 7)['K_t_day']
        old = shared_certificate(G=962., eta=eta, Q=103.618, delta=1, Lmax=60, K=K)
        new = certificate(962., eta, 103.618, 1, 60, K, Rc=0, Rp=0, tank_events=0, C=0.)
        gap = new['reserve_t'] - old['required_reserve_t']
        assert abs(gap) < 1e-6
        assert abs(new['separate_reserve_t'] - new['reserve_t'] - eta * 962. * 7) < 1e-6
        shared_comparison.append(dict(eta=eta, tighter_v7_shared_only_reserve_t=old['required_reserve_t'],
                                      v8_partitioned_shared_only_reserve_t=new['reserve_t'],
                                      regression_difference_t=gap,
                                      avoidable_separate_backlog_conservatism_t=new['separate_reserve_t'] - new['reserve_t'],
                                      interpretation='The newly proved partition bound recovers v7 on its original support and also permits independent fault calendars; no minimum-reserve claim.'))
    T = 365; trace_runs = []
    for phase in [0, 23, 180, 359]:
        cal = dict(common=_periodic(T, 365, phase, 7),
                   capture=_periodic(T, 365, phase + 40, 3),
                   processor=_periodic(T, 365, phase + 90, 3),
                   dispatch=_periodic(T, 365, phase, 60),
                   port=_periodic(T, 365, phase + 180, 7),
                   cargo=_periodic(T, 365, phase + 70),
                   tank=_periodic(T, 365, phase + 100),
                   hull=_periodic(T, 365, phase + 120))
        for captured in [0., .5, 1.]:
            cal['capture_fraction'] = np.full(T, captured)
            for mode in ['min', 'max', 'alternating', 'bunch']:
                result, rows = replay(representative, cal, mode, save_rows=(phase == 0 and mode == 'bunch' and captured == 0.))
                trace_runs.append(dict(phase=phase, delay_mode=mode, captured_on_fault_day=captured, **result))
                if rows: _write_csv(outdir / 'water_v8_daily.csv', rows)
    # Exhaust all combinations of 0-or-1 event per four-day periodic calendar
    # for independent common/capture/processor faults, receiving outages,
    # dispatch closures, cargo losses and isolated tank incidents.
    rx = receiver_bound(1, 2, 1, 3, 1, 4)
    cert = certificate(10., .5, 20., 1, rx['Lmax'], 12., P=4, B=1,
                       R0=1, Rc=1, Rp=1, J=1, tank_events=1, C=2.)
    toy = dict(certificate=cert, receiver=rx, reserve_t=cert['reserve_t'],
               fleet=fleet_bound(rx['Lmax'] + 2, horizon_days=12,
                                 losses_per_period=1, P=4, activation_days=1))
    tiny_count = 0; tiny_min = 1e9
    options = [None, 0, 1, 2, 3]
    flags = {day: _periodic(12, 4, day) for day in options}
    for common, cap, proc, port, dispatch, cargo, tank in itertools.product(options, repeat=7):
        cal = dict(common=flags[common], capture=flags[cap], processor=flags[proc],
                   port=flags[port], dispatch=flags[dispatch], cargo=flags[cargo],
                   tank=flags[tank], hull=flags[1])
        result, _ = replay(toy, cal)
        tiny_min = min(tiny_min, result['minimum_fresh_t']); tiny_count += 1
    extra_capture_replays = 0
    for common, cap, proc, captured in itertools.product(options, options, options, [.5, 1.]):
        cal = {name: np.zeros(12, dtype=bool) for name in ['common', 'capture', 'processor', 'dispatch', 'port', 'cargo', 'tank', 'hull']}
        cal.update(common=flags[common], capture=flags[cap], processor=flags[proc],
                   capture_fraction=np.full(12, captured))
        result, _ = replay(toy, cal)
        tiny_min = min(tiny_min, result['minimum_fresh_t']); extra_capture_replays += 1
    sensitivity = []
    for eta, gf, Rc, Rp, Brx, Q in itertools.product([.94, .98], [1., 1.1, 1.2],
                                                   [0, 3, 7], [0, 3, 7],
                                                   [0, 7, 14], [103.618, 125., 150.]):
        g = 962 * gf; plant = size_processor(g, eta, 7 + Rp)
        rx = receiver_bound(30, 60, 1, 4, Brx)
        cert = certificate(g, eta, Q, 1, rx['Lmax'], plant['K_t_day'], Rc=Rc, Rp=Rp)
        sensitivity.append(dict(eta=eta, G_factor=gf, Rc=Rc, Rp=Rp, port_closed_budget=Brx,
                                Q_t=Q, Lmax=rx['Lmax'], modules=plant['installed_modules'],
                                K_t_day=plant['K_t_day'], certified=cert['certified'],
                                reserve_t=cert.get('reserve_t', ''),
                                transport_margin_t_day=cert['transport_margin_t_day'],
                                processing_margin_t_day=cert['processing_margin_t_day']))
    _write_csv(outdir / 'water_v8_sensitivity.csv', sensitivity)
    # New receiving deadline must actually accommodate a full closure block.
    assert receiver_bound(30, 60, 1, 4, 7)['Lmax'] >= receiver_bound(30, 60, 1, 4, 0)['Lmax']
    assert fleet_bound(90, horizon_days=365)['spare_hulls'] == 1
    assert fleet_bound(90, horizon_days=366)['spare_hulls'] == 2
    # Parameterizing a larger demand and an unavailable module sizes actual
    # remaining capacity, rather than relabelling original equipment as robust.
    assert size_processor(962 * 1.2, .98, 10)['processing_margin_t_day'] >= 0
    # Deliberately invalid descriptors must be rejected even on mild paths.
    from copy import deepcopy
    mild = {name: np.zeros(8, dtype=bool) for name in ['common', 'capture', 'processor', 'dispatch', 'port', 'cargo', 'tank', 'hull']}
    invalid = []
    for name, change in [
            ('uncertified', lambda d: d['certificate'].update(certified=False)),
            ('reserve_below_certificate', lambda d: d.update(reserve_t=d['certificate']['reserve_t'] - 1)),
            ('receiver_delta', lambda d: d['receiver'].update(delta=2)),
            ('receiver_period', lambda d: d['receiver'].update(P=5)),
            ('fleet_delta', lambda d: d['fleet'].update(delta=2)),
            ('fleet_period', lambda d: d['fleet'].update(P=5)),
            ('fleet_horizon', lambda d: d['fleet'].update(horizon_days=7)),
            ('fleet_slots', lambda d: d['fleet'].update(base_fleet=1)),
            ('fleet_activation', lambda d: d['fleet'].update(rotation_hold_days=d['fleet']['cycle_days'])),
            ('fleet_spares', lambda d: d['fleet'].update(spare_hulls=0))]:
        wrong = deepcopy(toy); change(wrong)
        try: replay(wrong, mild)
        except ValueError: invalid.append(name)
        else: raise AssertionError('Invalid design accepted: ' + name)
    tail_calendar = {k: v.copy() for k, v in mild.items()}; tail_calendar['hull'][7] = True
    tail_result, _ = replay(toy, tail_calendar)
    assert tail_result['tail_hull_replacements'] == 1 and tail_result['permanent_hull_losses_on_dispatched_trips'] == 1
    # The controller must not use later changes to the fault calendars.
    nofault = {name: np.zeros(365, dtype=bool) for name in mild}
    future = {name: a.copy() for name, a in nofault.items()}
    future['common'][180:187] = True; future['processor'][210:213] = True
    future['capture'][240:243] = True; future['port'][270:277] = True
    _, rows0 = replay(representative, nofault, save_rows=True)
    _, rows1 = replay(representative, future, save_rows=True)
    prefix_same = [x['dispatch'] for x in rows0[:180]] == [x['dispatch'] for x in rows1[:180]]
    assert prefix_same
    record = dict(version='v8_independent_faults_closed_receiving_finite_hulls',
                  designs=designs, representative=representative,
                  representative_replays=trace_runs, tiny_complete_periodic_calendars=tiny_count,
                  tiny_minimum_fresh_t=tiny_min, sensitivity_rows=len(sensitivity),
                  additional_partial_capture_replays=extra_capture_replays,
                  future_fault_dispatch_prefix_unchanged=prefix_same,
                  shared_only_reference=shared_comparison, invalid_descriptors_rejected=invalid,
                  tail_spare_stock_test=tail_result,
                  finite_hull_scope='One-year examples, with prepositioned dispatch-side spare hulls; finite-year count cannot be used as infinite-year replenishment.',
                  engineering_unknowns=['module mass/power/price', 'partial-gravity water quality',
                                        'repair staffing, consumables and actual lunar fault budgets'],
                  comparison='Broader support may require larger reserve than v7. A new suffix-partition bound removes avoidable double-counting and recovers v7 exactly on shared-only support; no new minimum-reserve claim.')
    (outdir / 'water_v8.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(tiny_complete_periodic_calendars=tiny_count,
                          sensitivity_rows=len(sensitivity), representative_replays=len(trace_runs),
                          representative_reserve_t=representative['reserve_t']), ensure_ascii=False))
    return record


if __name__ == '__main__':
    run()
