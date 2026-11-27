"""Q4–Q5. Minimise v9 budget under simultaneous habitation and emissions limits."""

import argparse
import math
from pathlib import Path

from programming_handoff import default_fault_policies
from utils.supplemental_io import SUPPLEMENTAL, load_verified_study, write_result_table


DAYS_PER_YEAR = 365  # v9 joint_v9.P
KG_PER_GT = 1e12


def nonnegative_limit(text):
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number") from exc
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError("limit must be finite and nonnegative")
    return value


def screen_policies(study, deadlines_years, emissions_caps_kg, scenario):
    """Screen the saved default-mission fault catalogue using unrounded limits."""
    policies = default_fault_policies(study)
    if not policies:
        raise ValueError("The verified v9 catalogue contains no default-mission fault policies")

    def scores(policy):
        values = policy["scenarios"][scenario]
        return values["cost_usd"], policy["habitation_upper_days"], values["CO2proxy_kg"]

    if any(not math.isfinite(value) or value < 0 for p in policies for value in scores(p)):
        raise ValueError("The v9 catalogue contains invalid policy scores")
    # After minimum budget, break exact ties by time, emissions and the
    # actual decisions. Content hashes can change across platforms.
    ranked = sorted(policies, key=lambda p: (*scores(p), p["construction_E_share"],
                    p["preposition_E_share"], p["water_id"], p["equipment_packing_policy"]))

    caps = sorted(set(emissions_caps_kg))
    emission_counts = {cap: sum(scores(p)[2] <= cap for p in ranked) for cap in caps}
    rows = []
    for years in sorted(set(deadlines_years)):
        deadline_days = years * DAYS_PER_YEAR
        time_eligible = [p for p in ranked if scores(p)[1] <= deadline_days]
        for cap in caps:
            eligible = [p for p in time_eligible if scores(p)[2] <= cap]
            winner = eligible[0] if eligible else {}
            cost, days, emissions = scores(winner) if winner else (None, None, None)
            rows.append({
                "coefficient_scenario": scenario,
                "mission_key": study["default_mission_key"],
                "operating_mode": "fault",
                "deadline_years": years,
                "deadline_days": deadline_days,
                "emissions_cap_Gt_CO2e_proxy": cap / KG_PER_GT,
                "emissions_cap_kg_CO2e_proxy": cap,
                "catalogue_count": len(ranked),
                "time_only_eligible_count": len(time_eligible),
                "emissions_only_eligible_count": emission_counts[cap],
                "joint_eligible_count": len(eligible),
                "status": "selected" if eligible else "no_candidate_satisfies_both_limits",
                "selected_policy_id": winner.get("id"),
                "selected_budget_USD": cost,
                "selected_habitation_upper_days": days,
                "selected_habitation_upper_years": days / DAYS_PER_YEAR if days is not None else None,
                "selected_emissions_kg_CO2e_proxy": emissions,
                "selected_emissions_Gt_CO2e_proxy": emissions / KG_PER_GT if emissions is not None else None,
                "construction_E_share": winner.get("construction_E_share"),
                "preposition_E_share": winner.get("preposition_E_share"),
                "water_id": winner.get("water_id"),
                "operation_route": (winner["operation_route"] or "stock_only") if winner else None,
                "equipment_packing_policy": winner.get("equipment_packing_policy"),
            })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deadline-years", nargs="+", type=nonnegative_limit,
                        help="latest habitation time, using 365 days per v9 year")
    parser.add_argument("--emissions-cap-gt", nargs="+", type=nonnegative_limit,
                        help="maximum emissions proxy in gigatonnes of CO2 equivalent")
    parser.add_argument("--scenario", default="central", help="v9 coefficient scenario (default: central)")
    parser.add_argument("--output", type=Path, help="optional CSV path for the selected grid")
    args = parser.parse_args()

    study = load_verified_study()
    if args.scenario not in study["selections"]:
        parser.error("unknown scenario; choose from " + ", ".join(study["selections"]))
    deadlines = args.deadline_years if args.deadline_years is not None else [
        point["deadline_years"] for point in study["deadline_stress"]
    ]
    caps_kg = ([cap * KG_PER_GT for cap in args.emissions_cap_gt]
               if args.emissions_cap_gt is not None else
               [row["emissions_budget_kg"] for row in study["selections"][args.scenario]["epsilon_rows"]])
    if any(not math.isfinite(value) for value in [*(y * DAYS_PER_YEAR for y in deadlines), *caps_kg]):
        parser.error("limit exceeds the representable range after converting units")
    custom = (args.deadline_years is not None or args.emissions_cap_gt is not None
              or args.scenario != "central")
    output = args.output or SUPPLEMENTAL / (
        "q4_q5_joint_screening_custom.csv" if custom else "q4_q5_joint_screening.csv"
    )
    try:
        path = write_result_table(output, screen_policies(study, deadlines, caps_kg, args.scenario))
    except ValueError as exc:
        parser.error(str(exc))
    print(path)


if __name__ == "__main__":
    main()
