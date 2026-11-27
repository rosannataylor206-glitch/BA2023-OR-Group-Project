"""Restricted apex--Moon mission family with explicit mass and resource interfaces.

This is a circular, coplanar, zero-sphere-of-influence patched-conic study.
It is neither an ephemeris trajectory nor a certification of nuclear propulsion,
finite-thrust landing, structural mass, or the stated logistics time allowance.
"""
from pathlib import Path
import csv
import itertools
import json
import math

ROOT = Path(__file__).resolve().parent
DAY = 86400.0
MU_E = 398600.435507       # JPL DE440, km^3/s^2
MU_M = 4902.800118         # JPL DE440, km^3/s^2
R_E = 6378.0              # Rounded Earth model used in the problem study, km
R_M = 1737.4              # JPL volume-equivalent mean lunar radius, km
MOON_DISTANCE = 384400.0   # Circular replacement for the NASA mean orbit, km
SIDEREAL_DAY_S = 86164.09054  # JPL astrodynamic parameters
OMEGA = 2.0 * math.pi / SIDEREAL_DAY_S
G0_KM_S2 = 9.80665 / 1000.0


def _positive_finite(**values):
    if any(not math.isfinite(v) or v <= 0 for v in values.values()):
        raise ValueError("Positive finite physical quantities are required: " + ", ".join(values))


def transfer_geometry(apex_height_km=100000.0, parking_height_km=100.0):
    _positive_finite(apex_height_km=apex_height_km, parking_height_km=parking_height_km)
    if parking_height_km > 1000.0:
        raise ValueError("Lunar parking altitude is outside the declared <=1000km study range.")
    r0 = R_E + apex_height_km
    if r0 >= MOON_DISTANCE:
        raise ValueError("This restricted ellipse requires apex radius < lunar distance.")
    rp = R_M + parking_height_km
    a = (r0 + MOON_DISTANCE) / 2.0
    v_peri = math.sqrt(MU_E * (2.0 / r0 - 1.0 / a))
    v_apo = math.sqrt(MU_E * (2.0 / MOON_DISTANCE - 1.0 / a))
    lunar_n = math.sqrt((MU_E + MU_M) / MOON_DISTANCE**3)
    lunar_v = lunar_n * MOON_DISTANCE
    v_inf = abs(lunar_v - v_apo)
    v_lunar_hyper = math.sqrt(v_inf**2 + 2.0 * MU_M / rp)
    v_lunar_circ = math.sqrt(MU_M / rp)
    a_surface = (R_M + rp) / 2.0
    surface_vperi = math.sqrt(MU_M * (2.0 / R_M - 1.0 / a_surface))
    surface_vapo = math.sqrt(MU_M * (2.0 / rp - 1.0 / a_surface))
    lunar_descent = abs(v_lunar_circ - surface_vapo) + surface_vperi
    earth_half_days = math.pi * math.sqrt(a**3 / MU_E) / DAY
    lunar_half_days = math.pi * math.sqrt(a_surface**3 / MU_M) / DAY
    phase_cycle_days = 2.0 * math.pi / abs(OMEGA - lunar_n) / DAY
    return {
        "apex_height_km": apex_height_km,
        "apex_radius_km": r0,
        "lunar_circular_radius_km": MOON_DISTANCE,
        "lunar_parking_height_km": parking_height_km,
        "earth_ellipse_semimajor_km": a,
        "earth_ellipse_perigee_speed_km_s": v_peri,
        "earth_ellipse_apogee_speed_km_s": v_apo,
        "apex_corotation_speed_km_s": OMEGA * r0,
        "apex_switch_impulse_km_s": abs(OMEGA * r0 - v_peri),
        "moon_circular_speed_km_s": lunar_v,
        "moon_relative_v_infinity_km_s": v_inf,
        "lunar_capture_impulse_km_s": abs(v_lunar_hyper - v_lunar_circ),
        "lunar_ideal_descent_or_ascent_km_s": lunar_descent,
        "earth_half_ellipse_days": earth_half_days,
        "lunar_half_ellipse_days": lunar_half_days,
        "single_apex_phase_cycle_days": phase_cycle_days,
        "phase_window_scope": "One alignment per relative apex--Moon phase cycle in this circular coplanar model; not the real lunar launch-window calendar.",
        "scope": "Zero-SOI patched conics; lunar eccentricity, inclination, Sun, finite SOI timing, finite thrust, exact surface site and tether rendezvous tolerances are not solved.",
    }


def mission_record(Isp_s=900.0, dry_to_net_cargo_ratio=0.2,
                   surface_loss_margin_km_s=0.3,
                   architecture="single_vehicle_roundtrip",
                   min_structural_fraction=0.05,
                   surface_service_days=3.0,
                   apex_service_days=7.0,
                   encounter_time_allowance_per_leg_days=2.0):
    """Return a mass-consistent, explicitly conditional mission interface.

    The loss margin is ADDED to each lunar descent/ascent; it is not measured.
    Structural fraction is dry vehicle / initial apex wet mass, INCLUDING cargo.
    This chosen screening convention is stated explicitly and is not a universal
    rocket structural coefficient or a validated engineering limit.
    """
    _positive_finite(Isp_s=Isp_s, dry_to_net_cargo_ratio=dry_to_net_cargo_ratio)
    extra = [surface_loss_margin_km_s, surface_service_days, apex_service_days,
             encounter_time_allowance_per_leg_days]
    if any(not math.isfinite(x) or x < 0 for x in extra):
        raise ValueError("Nonnegative finite loss and time allowances are required.")
    if not math.isfinite(min_structural_fraction) or not 0 < min_structural_fraction < 1:
        raise ValueError("The declared structural screen must lie strictly in (0,1).")
    if architecture not in ["single_vehicle_roundtrip", "expendable_oneway"]:
        raise ValueError("Unsupported mission architecture.")
    geo = transfer_geometry()
    ve = G0_KM_S2 * Isp_s
    dv_surface = geo["lunar_ideal_descent_or_ascent_km_s"] + surface_loss_margin_km_s
    dv_out = geo["apex_switch_impulse_km_s"] + geo["lunar_capture_impulse_km_s"] + dv_surface
    roundtrip = architecture == "single_vehicle_roundtrip"
    dv_return = dv_out if roundtrip else 0.0
    A = math.exp(dv_out / ve)
    B = math.exp(dv_return / ve)
    chi = dry_to_net_cargo_ratio
    landed = 1.0 + chi * B
    beta = A * landed
    return_prop = chi * (B - 1.0) if roundtrip else 0.0
    structural = chi / beta
    # Ideal coast durations exclude alignment, handling and the zero-SOI patch.
    coast = geo["earth_half_ellipse_days"] + geo["lunar_half_ellipse_days"]
    phase = geo["single_apex_phase_cycle_days"]
    ready_to_surface = coast + phase + encounter_time_allowance_per_leg_days
    cycle = (2.0 * coast + 2.0 * phase + surface_service_days + apex_service_days
             + 2.0 * encounter_time_allowance_per_leg_days) if roundtrip else None
    name = ("rt" if roundtrip else "ow") + f"_isp{Isp_s:g}_dry{chi:.2f}_loss{surface_loss_margin_km_s:.2f}"
    rec = {
        "name": name,
        "architecture": architecture,
        "Isp_s": Isp_s,
        "dry_to_net_cargo_ratio": chi,
        "surface_loss_margin_each_way_km_s": surface_loss_margin_km_s,
        "delta_v_out_km_s": dv_out,
        "delta_v_return_km_s": dv_return,
        "beta_outbound_per_net_cargo": beta,
        "landing_mass_per_net_cargo": landed,
        "approach_mass_before_descent_per_net_cargo": landed * math.exp(dv_surface / ve),
        "unloaded_mass_per_net_cargo": 1.0,
        "return_dry_per_net_cargo": chi if roundtrip else 0.0,
        "initial_dry_hardware_per_net_cargo": chi if roundtrip else 0.0,
        "recurring_apex_resupply_mass_per_net_cargo": beta - (chi if roundtrip else 0.0),
        "net_cargo_mass_scope": "Delivered payload including any required container/packaging mass; pure usable water is a separate fraction of that payload.",
        "recurring_lift_scope": "Returned dry hardware remains at the apex for reuse. Initial reusable dry hardware is lifted/deployed once; recurring resupply excludes that dry mass.",
        "dry_hardware_left_on_moon_per_net_cargo": 0.0 if roundtrip else chi,
        "return_propellant_carried_per_net_cargo": return_prop,
        "outbound_propellant_per_net_cargo": beta - landed,
        "structural_dry_fraction": structural,
        "structural_fraction_denominator": "Initial apex wet mass including net cargo; explicitly chosen screening convention.",
        "min_structural_fraction": min_structural_fraction,
        "structural_screen_pass": structural >= min_structural_fraction,
        "structural_screen_is_scenario": True,
        "structural_feasibility_verified": False,
        "roundtrip_dry_fraction_supremum_as_chi_increases": math.exp(-(dv_out + dv_return) / ve),
        "outbound_flight_days": coast,
        "outbound_flight_days_scope": "Ideal Earth and lunar half-ellipse coast only; does not include finite-SOI approach timing, alignment or operations.",
        "outbound_phase_wait_bound_days": phase,
        "encounter_time_allowance_per_leg_days_scenario": encounter_time_allowance_per_leg_days,
        "outbound_ready_to_touchdown_days_scenario": ready_to_surface,
        "outbound_ready_to_touchdown_days_integer_scenario": math.ceil(ready_to_surface),
        "return_phase_wait_bound_days": phase if roundtrip else 0.0,
        "surface_service_days_scenario": surface_service_days,
        "apex_service_days_scenario": apex_service_days if roundtrip else 0.0,
        "return_cycle_days": math.ceil(cycle) if roundtrip else None,
        "return_cycle_unrounded_days_scenario": cycle,
        "vehicle_return_required": roundtrip,
        "new_vehicle_required_per_delivery": not roundtrip,
        "max_departures_per_phase_window_scenario": 2,
        "phase_capacity_scope": "At most one mission dispatch per integer day requires permission for up to two physical departures at a phase window; a one-ship-per-window rule cannot sustain one ship/day at a single apex.",
        "propulsion_class": "Chemical performance scenario" if Isp_s <= 450 else "Advanced high-Isp performance scenario; 900 s does not certify a usable nuclear lunar lander.",
        "recommended_for_conditional_study": False,
        "scope": "Restricted task family with uncalibrated vehicle dry ratio, propulsion, loss and handling allowances. Passing the structural scenario is not real engineering verification, global orbital optimality, or nuclear safety approval.",
    }
    # Algebraic assertions use a second, sequential mass reconstruction.
    final_dry = chi
    return_start = final_dry * math.exp(dv_return / ve) if roundtrip else final_dry
    touchdown = return_start + 1.0
    departure = touchdown * math.exp(dv_out / ve)
    assert math.isclose(departure, beta, rel_tol=1e-13)
    assert math.isclose(touchdown, landed, rel_tol=1e-13)
    assert math.isclose(beta - (beta - landed) - 1.0 - return_prop, chi, rel_tol=1e-12)
    return rec


def staged_record(Isp_tug_s=900.0, Isp_lander_s=450.0,
                  dry_tug_to_net_cargo=0.2, dry_lander_to_net_cargo=0.2,
                  surface_loss_margin_km_s=0.3, min_structural_fraction=0.05,
                  lunar_orbit_separation_days=0.5, return_rendezvous_dock_days=0.5):
    """NTR tug stays in lunar orbit; a chemical lander descends and returns.

    All usable propellants, including BOTH return legs, leave the apex initially.
    No lunar refuelling or expendable hardware is silently assumed. Structural
    screens apply separately to component dry/(dry + its own total propellant),
    excluding its carried payload; old uniform-Isp rows keep their stated screen.
    """
    _positive_finite(Isp_tug_s=Isp_tug_s, Isp_lander_s=Isp_lander_s,
                     dry_tug_to_net_cargo=dry_tug_to_net_cargo,
                     dry_lander_to_net_cargo=dry_lander_to_net_cargo)
    if any(not math.isfinite(x) or x < 0 for x in [lunar_orbit_separation_days, return_rendezvous_dock_days]):
        raise ValueError("Nonnegative finite lunar orbit operation times required.")
    dT, dL = dry_tug_to_net_cargo, dry_lander_to_net_cargo
    geo = transfer_geometry()
    dvT = geo["apex_switch_impulse_km_s"] + geo["lunar_capture_impulse_km_s"]
    dvL = geo["lunar_ideal_descent_or_ascent_km_s"] + surface_loss_margin_km_s
    # Reuse the explicitly labelled time conventions and input guards. Every
    # mass-dependent field is then replaced by the staged equations below.
    rec = mission_record(Isp_tug_s, dT + dL, surface_loss_margin_km_s,
                         min_structural_fraction=min_structural_fraction)
    AT = math.exp(dvT / (G0_KM_S2 * Isp_tug_s))
    BT = AT
    AL = math.exp(dvL / (G0_KM_S2 * Isp_lander_s))
    BL = AL
    M_L = AL * (1.0 + dL * BL)
    P_Tr = (dT + dL) * (BT - 1.0)
    beta = AT * (M_L + dT + P_Tr)
    touchdown = 1.0 + dL * BL
    P_Lr = dL * (BL - 1.0)
    prop_tug_total = beta - M_L - dT
    prop_lander_total = M_L - 1.0 - dL
    epsT = dT / (dT + prop_tug_total)
    epsL = dL / (dL + prop_lander_total)
    outbound_consumed = (beta - (M_L + dT + P_Tr)) + (M_L - touchdown)
    extra_ops = lunar_orbit_separation_days + return_rendezvous_dock_days
    ready = rec["outbound_ready_to_touchdown_days_scenario"] + lunar_orbit_separation_days
    cycle = rec["return_cycle_unrounded_days_scenario"] + extra_ops
    rec.update({
        "name": f"staged_tug{Isp_tug_s:g}_lander{Isp_lander_s:g}_dT{dT:.2f}_dL{dL:.2f}_loss{surface_loss_margin_km_s:.2f}",
        "architecture": "orbital_tug_chemical_lander",
        "Isp_s": Isp_tug_s,
        "Isp_s_scope": "Legacy common field means tug Isp only; lander has its separately stated Isp.",
        "Isp_tug_s": Isp_tug_s,
        "Isp_lander_s": Isp_lander_s,
        "dry_to_net_cargo_ratio": dT + dL,
        "dry_tug_to_net_cargo_ratio": dT,
        "dry_lander_to_net_cargo_ratio": dL,
        "tug_delta_v_each_way_km_s": dvT,
        "lander_delta_v_each_way_km_s": dvL,
        "delta_v_out_km_s": dvT + dvL,
        "delta_v_return_km_s": dvT + dvL,
        "delta_v_total_scope": "Sum of impulses on two different propulsion stages; do not apply one Isp to this total.",
        "beta_outbound_per_net_cargo": beta,
        "landing_mass_per_net_cargo": touchdown,
        "approach_mass_before_descent_per_net_cargo": M_L,
        "return_dry_per_net_cargo": dT + dL,
        "initial_dry_hardware_per_net_cargo": dT + dL,
        "recurring_apex_resupply_mass_per_net_cargo": beta - dT - dL,
        "return_propellant_carried_per_net_cargo": P_Tr + P_Lr,
        "outbound_propellant_per_net_cargo": outbound_consumed,
        "initial_lander_mass_at_lunar_orbit_per_net_cargo": M_L,
        "tug_mass_parked_in_lunar_orbit_per_net_cargo": dT + P_Tr,
        "tug_return_wet_mass_after_rendezvous_per_net_cargo": (dT + dL) * BT,
        "return_tug_propellant_per_net_cargo": P_Tr,
        "return_lander_propellant_per_net_cargo": P_Lr,
        "tug_propellant_total_per_net_cargo": prop_tug_total,
        "lander_propellant_total_per_net_cargo": prop_lander_total,
        "tug_structural_dry_fraction": epsT,
        "lander_structural_dry_fraction": epsL,
        "structural_dry_fraction": min(epsT, epsL),
        "structural_dry_fraction_including_all_payload": (dT + dL) / beta,
        "structural_fraction_denominator": "Minimum of tug and lander dry/(component dry + component own total propellant); excludes carried payload, unlike the old uniform-Isp rows.",
        "structural_screen_pass": min(epsT, epsL) >= min_structural_fraction,
        "roundtrip_dry_fraction_supremum_as_chi_increases": None,
        "outbound_ready_to_touchdown_days_scenario": ready,
        "outbound_ready_to_touchdown_days_integer_scenario": math.ceil(ready),
        "lunar_orbit_separation_days_scenario": lunar_orbit_separation_days,
        "return_rendezvous_dock_days_scenario": return_rendezvous_dock_days,
        "return_cycle_days": math.ceil(cycle),
        "return_cycle_unrounded_days_scenario": cycle,
        "propulsion_class": "Conceptual high-Isp orbital tug plus chemical surface lander; NTR reactor stays in lunar orbit.",
        "recommended_for_conditional_study": Isp_tug_s == 900 and Isp_lander_s == 450 and dT == .2 and dL == .2 and surface_loss_margin_km_s == .3 and min(epsT, epsL) >= min_structural_fraction,
        "scope": "Staged architecture inspired by NASA2018 conceptual NTR LTV + chemical LLV, with project-specific apex trajectory, masses, operations and no lunar refuelling. Hardware, reserves/boil-off, three-body geometry, finite thrust and docking performance remain unvalidated.",
    })
    # Independently march mass through both vehicle timelines, not one
    # exponential with an averaged Isp.
    after_tug_out = beta / AT
    assert math.isclose(after_tug_out, M_L + dT + P_Tr, rel_tol=1e-12)
    after_lander_down = M_L / AL
    assert math.isclose(after_lander_down, touchdown, rel_tol=1e-12)
    lander_return_after_unload = after_lander_down - 1.0
    lander_dry_back = lander_return_after_unload / BL
    assert math.isclose(lander_dry_back, dL, rel_tol=1e-12)
    combined_after_return = (dT + P_Tr + lander_dry_back) / BT
    assert math.isclose(combined_after_return, dT + dL, rel_tol=1e-12)
    assert math.isclose(beta - outbound_consumed - 1.0 - P_Tr - P_Lr, dT + dL, rel_tol=1e-12)
    assert math.isclose(rec["recurring_apex_resupply_mass_per_net_cargo"],
                        1.0 + outbound_consumed + P_Tr + P_Lr, rel_tol=1e-12)
    return rec


def mission_catalog():
    records = [mission_record(I, chi, margin)
               for I, chi, margin in itertools.product([450.0, 900.0], [0.1, 0.2, 0.5], [0.1, 0.3, 0.5])]
    records += [mission_record(450.0, chi, 0.3, architecture="expendable_oneway")
                for chi in [0.1, 0.2, 0.5]]
    records += [staged_record(I, 450.0, dT, dL)
                for I, dT, dL in itertools.product([450.0, 900.0], [.1, .2, .5], [.1, .2, .5])]
    return records


def validation():
    """Independent ODE/energy and mass reconstruction, plus assumption guards."""
    import numpy as np
    from scipy.integrate import solve_ivp
    geo = transfer_geometry()
    r0 = geo["apex_radius_km"]
    vp = geo["earth_ellipse_perigee_speed_km_s"]
    tf = geo["earth_half_ellipse_days"] * DAY
    def rhs(t, z):
        r = math.hypot(z[0], z[1])
        return [z[2], z[3], -MU_E * z[0] / r**3, -MU_E * z[1] / r**3]
    ode = solve_ivp(rhs, [0.0, tf], [r0, 0.0, 0.0, vp], method="DOP853", rtol=1e-12, atol=1e-12,
                    dense_output=True)
    end = ode.y[:, -1]
    position_error = math.hypot(end[0] + MOON_DISTANCE, end[1])
    expected_va = geo["earth_ellipse_apogee_speed_km_s"]
    velocity_error = math.hypot(end[2], end[3] + expected_va)
    sample = ode.sol(np.linspace(0.0, tf, 101))
    radii = np.hypot(sample[0], sample[1])
    energies = .5 * (sample[2]**2 + sample[3]**2) - MU_E / radii
    target_energy = -MU_E / (2.0 * geo["earth_ellipse_semimajor_km"])
    energy_error = float(np.max(abs(energies - target_energy)))
    h_error = abs(r0 * vp - MOON_DISTANCE * expected_va)
    assert ode.success and position_error < 1e-4 and velocity_error < 1e-8
    assert energy_error < 1e-9 and h_error < 1e-8
    # A direct angle equation verifies the circular phase waiting construction.
    lunar_n = math.sqrt((MU_E + MU_M) / MOON_DISTANCE**3)
    phase_max = geo["single_apex_phase_cycle_days"] * DAY
    phase_error = 0.0
    max_window_departures = 0
    phase_period_days = phase_max / DAY
    for offset in np.linspace(0.0, 2.0 * math.pi, 129, endpoint=False):
        wait = (offset % (2.0 * math.pi)) / (OMEGA - lunar_n)
        assert 0.0 <= wait < phase_max
        phase_error = max(phase_error, abs((OMEGA - lunar_n) * wait - offset))
        # Independently place ten years of daily requests into their next phase
        # windows. The window service assumption must allow two departures.
        first_window = wait / DAY
        days = np.arange(3650, dtype=float)
        window_index = np.maximum(0, np.ceil((days - first_window) / phase_period_days - 1e-12)).astype(int)
        counts = np.bincount(window_index)
        max_window_departures = max(max_window_departures, int(counts.max()))
        physical_departure = first_window + window_index * phase_period_days
        assert float(np.min(physical_departure - days)) >= -1e-9
        assert float(np.max(physical_departure - days)) <= phase_period_days + 1e-9
    assert max_window_departures == 2
    invalid = [lambda: mission_record(Isp_s=0), lambda: mission_record(dry_to_net_cargo_ratio=-1),
               lambda: mission_record(surface_loss_margin_km_s=-1), lambda: mission_record(min_structural_fraction=1),
               lambda: mission_record(Isp_s=float("nan")), lambda: transfer_geometry(apex_height_km=500000),
               lambda: transfer_geometry(parking_height_km=10000), lambda: staged_record(Isp_lander_s=0)]
    rejected = 0
    for action in invalid:
        try:
            action()
        except ValueError:
            rejected += 1
    assert rejected == len(invalid)
    records = mission_catalog()
    for row in records:
        if row["recommended_for_conditional_study"]:
            assert row["structural_screen_pass"]
    # Old beta=1.5 is incompatible with every row of THIS fixed trajectory family.
    assert min(x["beta_outbound_per_net_cargo"] for x in records) > 1.5
    return {
        "ode_half_ellipse_position_error_km": position_error,
        "ode_half_ellipse_velocity_error_km_s": velocity_error,
        "ode_energy_error_km2_s2": energy_error,
        "angular_momentum_check_error_km2_s": h_error,
        "phase_angle_cases": 129,
        "daily_phase_window_schedules_checked": 129,
        "daily_requests_per_schedule": 3650,
        "maximum_departures_assigned_to_one_phase_window": max_window_departures,
        "phase_equation_max_error_rad": phase_error,
        "mass_chain_records_checked": len(records),
        "invalid_inputs_rejected": rejected,
        "all_implemented_checks_pass": True,
        "scope": "Arithmetic and declared circular-model consistency; no real trajectory/hardware certification.",
    }


def run(output_dir=None):
    out = Path(output_dir) if output_dir else ROOT / "results"
    out.mkdir(parents=True, exist_ok=True)
    catalog = mission_catalog()
    summary = {
        "version": "v8_restricted_physics_interface",
        "geometry": transfer_geometry(),
        "missions": catalog,
        "checks": validation(),
        "important_limits": [
            "Real lunar inclination18.28--28.58deg to Earth's equator and eccentricity0.0549 are replaced by a coplanar circle. No unpriced plane change is certified.",
            "Zero-SOI matching is an approximation; finite-SOI and finite-thrust encounter time is an explicit allowance, not a physical upper-bound theorem.",
            "900s orbital NTR and450s chemical lander are concept-level performance scenarios; dry ratios, losses, service allowances and5% component screens remain uncalibrated. Old uniform900s surface rows are stress comparisons only.",
            "Apex capture geometry, tether loads, exact surface site, fuel boil-off, thermal and radiation constraints remain unmodeled.",
            "Reference cases bind beta and touchdown mass to the SAME mass chain, but do not imply global superiority or real feasibility.",
        ],
    }
    (out / "physics_v8.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out / "physics_v8_missions.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = list(dict.fromkeys(k for record in catalog for k in record))
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(catalog)
    print(json.dumps({"records": len(catalog), "checks": summary["checks"],
                      "conditional_reference": next(x for x in catalog if x["recommended_for_conditional_study"])}, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    run()
