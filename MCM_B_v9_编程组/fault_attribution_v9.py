"""Q2. Remove one counted construction fault at a time and compare allocations."""

from dataclasses import replace
from math import isclose

import joint_v9 as joint
from construction_v9 import ConstructionInputs
from programming_handoff import ATOL, RTOL
from utils.supplemental_io import SUPPLEMENTAL, load_verified_study, write_result_table


# Each row removes one parameter from the v9 fault support. All other
# assumptions, including lead-time jitter and propellant losses, are retained.
FAULT_CASES = (
    ("baseline", None, None),
    ("no_lift_closures", "lift_closed_days", "closed days / rolling 365 days"),
    ("no_apex_dispatch_closures", "E_closed_days", "closed days / rolling 365 days"),
    ("no_ground_site_closures", "R_closed_days", "closed days / rolling 365 days"),
    ("no_lunar_port_closures", "port_closed_days", "closed days / rolling 365 days"),
    ("no_elevator_cargo_losses", "cargo_losses_E_per_harbour_year", "batches / harbour / rolling 365 days"),
    ("no_rocket_cargo_losses", "cargo_losses_R_per_site_year", "batches / site / rolling 365 days"),
    ("no_elevator_hull_losses", "hull_losses_E_per_harbour_year", "hulls / harbour / rolling 365 days"),
)


def construction_metrics(share, stock, mission_key):
    policy = joint.build_policy(share, stock, 0.0, "fault", mission_key, construction_only=True)
    phase = joint.REGISTRY[policy["phase_ids"][0]]
    bounds = {}
    for entry in phase["entries"]:
        route = entry["route"]
        days = entry["transport"]["construction_completion_upper_days"]
        bounds[route] = max(days, bounds.get(route, 0))
    delivery = policy["generic_construction_delivery_upper_days"]
    if not bounds or delivery != max(bounds.values()):
        raise ValueError("Construction delivery bound disagrees with its route bounds")
    return {
        "construction_E_share": share,
        "construction_delivery_upper_days": delivery,
        "construction_delivery_upper_years": delivery / joint.P,
        "central_construction_budget_USD": policy["scenarios"]["central"]["cost_usd"],
        "elevator_delivery_upper_days": bounds.get("E"),
        "rocket_delivery_upper_days": bounds.get("R"),
        "binding_routes": "+".join(route for route in sorted(bounds) if bounds[route] == delivery),
    }


def analyse_faults(study):
    key = study["default_mission_key"]
    base_choice = next(row for row in study["construction_summary"]
                       if row["mode"] == "fault" and row["route"] == "ER")
    reference = next(row for row in study["construction_baselines"]
                     if row["id"] == base_choice["policy_id"] and row["mission_key"] == key)
    share = reference["construction_E_share"]
    stock = next(row for row in study["water_catalogues"][f"fault_{key}"] if row["id"] == "stock_all")
    baseline = ConstructionInputs()
    saved_inputs = joint.ACTIVE_CONSTRUCTION_INPUTS
    rows = []
    try:
        if joint.register_mission(study["missions"][key]) != key:
            raise ValueError("The archived default mission key is inconsistent")
        joint.configure_inputs(baseline)
        base = construction_metrics(share, stock, key)
        base_days = base["construction_delivery_upper_days"]
        base_budget = base["central_construction_budget_USD"]
        if (base_days != reference["generic_construction_delivery_upper_days"]
                or not isclose(base_budget, reference["scenarios"]["central"]["cost_usd"],
                               rel_tol=RTOL, abs_tol=ATOL)):
            raise ValueError("The Q2 baseline no longer matches the verified v9 construction result")

        for case, field, unit in FAULT_CASES:
            joint.configure_inputs(replace(baseline, **{field: 0}) if field else baseline)
            shares = sorted(set(joint.share_catalogue("fault", key)) | {share})
            candidates = {s: construction_metrics(s, stock, key) for s in shares}
            fixed = candidates[share]
            fastest = min(candidates.values(), key=lambda row: (
                row["construction_delivery_upper_days"],
                row["central_construction_budget_USD"], row["construction_E_share"],
            ))
            for method, evaluated, result in (("fixed_baseline_share", 1, fixed),
                                               ("reselected_shortest_bound", len(shares), fastest)):
                rows.append({
                    "case": case,
                    "fault_parameter": field,
                    "baseline_allowance": getattr(baseline, field) if field else None,
                    "scenario_allowance": 0 if field else None,
                    "allowance_unit": unit,
                    "selection": method,
                    "candidate_count": evaluated,
                    "baseline_policy_id": reference["id"],
                    "mission_key": key,
                    **result,
                    "delivery_upper_reduction_years_vs_baseline": (
                        base_days - result["construction_delivery_upper_days"]
                    ) / joint.P,
                    "budget_change_USD_vs_baseline": result["central_construction_budget_USD"] - base_budget,
                })
    finally:
        joint.configure_inputs(saved_inputs)
    return rows


def main():
    path = write_result_table(SUPPLEMENTAL / "q2_fault_attribution.csv", analyse_faults(load_verified_study()))
    print(path)


if __name__ == "__main__":
    main()
