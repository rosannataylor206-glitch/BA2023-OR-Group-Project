"""Compare an independently rerun v9 with its archive and export paper data."""

import argparse
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
ATOL = 1e-7
RTOL = 1e-10


def read_json(directory, name):
    return json.loads((directory / name).read_text(encoding="utf-8"))


def check_equal(expected, actual, path, aliases=None):
    """Compare numeric values at the v9 verifier's tolerances."""
    aliases = aliases or {}
    if isinstance(expected, dict) and isinstance(actual, dict):
        translated = {aliases.get(key, key): value for key, value in actual.items()}
        if expected.keys() != translated.keys():
            raise ValueError(f"{path}: unexpected or missing keys")
        for key in expected:
            check_equal(expected[key], translated[key], f"{path}.{key}", aliases)
        return
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            raise ValueError(f"{path}: list lengths differ ({len(expected)}, {len(actual)})")
        for index, (left, right) in enumerate(zip(expected, actual)):
            check_equal(left, right, f"{path}[{index}]", aliases)
        return
    if isinstance(expected, str) and isinstance(actual, str):
        actual = aliases.get(actual, actual)
    if type(expected) in (int, float) and type(actual) in (int, float):
        if isinstance(expected, int) and isinstance(actual, int):
            matches = expected == actual
        else:
            matches = math.isfinite(expected) and math.isfinite(actual) and math.isclose(
                expected, actual, rel_tol=RTOL, abs_tol=ATOL
            )
    else:
        matches = type(expected) is type(actual) and expected == actual
    if not matches:
        raise ValueError(f"{path}: archive {expected!r} differs from rerun {actual!r}")


def by_key(records, key):
    indexed = {key(row): row for row in records}
    if len(indexed) != len(records):
        raise ValueError("Duplicate logical identity in policy or mission catalogue")
    return indexed


def compare_policies(expected, actual, mission_aliases, label):
    def identity(row, aliases):
        return (
            row.get("sensitivity_point_id"), row["mode"],
            aliases.get(row["mission_key"], row["mission_key"]),
            row["construction_E_share"], row["preposition_E_share"],
            row["water_id"], row["equipment_packing_policy"],
        )

    left = by_key(expected, lambda row: identity(row, {}))
    right = by_key(actual, lambda row: identity(row, mission_aliases))
    if left.keys() != right.keys():
        raise ValueError(f"{label}: logical policy identities changed")
    ids = {}
    reference_fields = {"id", "source_policy_id", "phase_ids"}
    for key, a in left.items():
        b = right[key]
        ids[b["id"]] = a["id"]
        if "source_policy_id" in b:
            ids[b["source_policy_id"]] = a["source_policy_id"]
        check_equal(len(a["phase_ids"]), len(b["phase_ids"]), f"{label}{key}.phase_count")
        check_equal(
            {k: v for k, v in a.items() if k not in reference_fields},
            {k: v for k, v in b.items() if k not in reference_fields},
            f"{label}{key}", mission_aliases,
        )
    return ids


def compare_sensitivity_ties(old, new, policy_aliases):
    """Resolve changed representatives of exact ties without masking metric changes."""
    left = by_key(old["policies"], lambda row: row["id"])
    right = by_key(new["policies"], lambda row: row["id"])
    old_cases = by_key(old["cases"], lambda row: row["point_id"])
    ties = []

    def compare_choice(point, old_id, new_id, scenario=None):
        if old_id == policy_aliases.get(new_id, new_id):
            return False
        metric = "habitation_upper_days" if scenario is None else f"cost_usd.{scenario}"
        if old_id is None or new_id is None:
            raise ValueError(f"{point}: {metric} selection feasibility changed")

        def objective(row):
            if scenario is None:
                return row["habitation_upper_days"]
            return row["scenarios"][scenario]["cost_usd"]

        a, b = left[old_id], right[new_id]
        for catalogue, chosen in ((left, a), (right, b)):
            eligible = [row for row in catalogue.values()
                        if row["sensitivity_point_id"] == point and row["integrated_stress_feasible"]]
            best = min(eligible, key=lambda row: (objective(row), row["id"]))
            if chosen["id"] != best["id"]:
                raise ValueError(f"{point}: {metric} choice fails the v9 selection rule")
        if objective(a) != objective(b):
            raise ValueError(f"{point}: {metric} objective value changed")
        ties.append({"point_id": point, "metric": metric, "value": objective(b),
                     "archive_id": old_id, "rerun_id": new_id})
        return True

    for case in new["cases"]:
        point = case["point_id"]
        expected = old_cases[point]
        if compare_choice(point, expected["fastest_policy_id"], case["fastest_policy_id"]):
            case["fastest_policy_id"] = expected["fastest_policy_id"]
        for scenario, chosen in case["best_by_coefficient_scenario"].items():
            previous = expected["best_by_coefficient_scenario"][scenario]
            if compare_choice(point, previous and previous["policy_id"],
                              chosen and chosen["policy_id"], scenario):
                # Only permit changes in policy labels. All reported numeric summaries
                # remain subject to the ordinary comparison below.
                row = right[chosen["policy_id"]]
                for label in ("water_id", "operation_route", "equipment_packing_policy"):
                    check_equal(row[label], chosen[label], f"{point}.{scenario}.{label}")
                    chosen[label] = previous[label]
                chosen["policy_id"] = previous["policy_id"]
    return ties


def compare_archive(archive, current):
    """Match policy content across platforms even when floating point hashes change."""
    old_dir = archive / "results"
    checks = {}
    for name in ("physics_v9.json", "water_v9.json", "independent_v9.json"):
        check_equal(read_json(old_dir, name), read_json(RESULTS, name), name)
        checks[name] = "matched"

    old = read_json(old_dir, "joint_v9.json")
    old_missions = {mission["name"]: key for key, mission in old["missions"].items()}
    new_missions = {mission["name"]: key for key, mission in current["missions"].items()}
    if len(old_missions) != len(old["missions"]) or len(new_missions) != len(current["missions"]):
        raise ValueError("Mission names must uniquely identify the compared missions")
    if old_missions.keys() != new_missions.keys():
        raise ValueError("Mission catalogue changed")
    aliases = {new_missions[name]: old_missions[name] for name in old_missions}
    aliases.update({f"{mode}_{new_missions[name]}": f"{mode}_{old_missions[name]}"
                    for mode in ("ideal", "fault") for name in old_missions})
    for name in ("construction_baselines", "candidates"):
        ids = compare_policies(old[name], current[name], aliases, name)
        aliases.update(ids)
        checks[name] = {"matched_records": len(current[name]),
                        "changed_hash_ids": sum(key != value for key, value in ids.items())}

    remaining = {"construction_baselines", "candidates"}
    check_equal({k: v for k, v in old.items() if k not in remaining},
                {k: v for k, v in current.items() if k not in remaining}, "joint metadata and selections", aliases)
    del old

    a = read_json(old_dir, "sensitivity_v9.json")
    b = read_json(RESULTS, "sensitivity_v9.json")
    ids = compare_policies(a["policies"], b["policies"], aliases, "sensitivity")
    aliases.update(ids)
    ties = compare_sensitivity_ties(a, b, aliases)
    remaining = {"policies", "elapsed_seconds"}
    check_equal({k: v for k, v in a.items() if k not in remaining},
                {k: v for k, v in b.items() if k not in remaining}, "sensitivity metadata and selections", aliases)
    checks["sensitivity_v9.json"] = {"matched_records": len(b["policies"]), "input_points": len(b["cases"]),
                                    "exact_objective_ties_with_different_selected_policy": ties}
    return {"all_comparisons_pass": True, "atol": ATOL, "rtol": RTOL, "checks": checks,
            "scope": "Numerical and logical policy comparison. Registry links and every phase recurrence "
                     "are checked within the rerun by verify_v9.py. Runtime measurements are excluded."}


def default_fault_policies(study):
    mission = study["default_mission_key"]
    return [row for row in study["candidates"] if row["mode"] == "fault" and row["mission_key"] == mission]


def selected_cases(study):
    policies = default_fault_policies(study)
    central = study["selections"]["central"]["min_cost_policy_id"]
    return {
        "minimum_central_budget": next(p for p in policies if p["id"] == central),
        "earliest_habitation_bound": min(policies, key=lambda p: p["habitation_upper_days"]),
        "minimum_central_budget_stock_only": min(
            (p for p in policies if p["water_id"] == "stock_all"),
            key=lambda p: p["scenarios"]["central"]["cost_usd"],
        ),
    }


def export_paper_data(study):
    rows = []

    def add(question, case, policy, source, metrics):
        rows.extend({"question": question, "scenario": case, "policy_id": policy,
                     "metric": name, "value": value, "unit": unit, "source": source}
                    for name, (value, unit) in metrics.items())

    for row in study["construction_summary"]:
        add("q1" if row["mode"] == "ideal" else "q2", f'{row["mode"]}_{row["route"]}_catalogue',
            row["policy_id"], "joint_v9.json#construction_summary", {
                "elevator_share": (row["E_share"], "fraction"),
                "construction_delivery_upper": (row["delivery_upper_years"], "year"),
                "central_construction_budget": (row["scenario_cost_USD"], "USD"),
            })
    mission = study["default_mission_key"]
    baselines = by_key([p for p in study["construction_baselines"] if p["mission_key"] == mission],
                       lambda p: (p["mode"], p["construction_E_share"]))
    for share in (0.0, 0.30, 1.0):
        for mode in ("ideal", "fault"):
            p = baselines[mode, share]
            add("q2", f"{mode}_fixed_E_share_{share:.2f}", p["id"],
                "joint_v9.json#construction_baselines", {
                    "elevator_share": (share, "fraction"),
                    "construction_delivery_upper": (p["generic_construction_delivery_upper_days"], "day"),
                    "central_construction_budget": (p["scenarios"]["central"]["cost_usd"], "USD"),
                    "construction_cargo_loss_upper": (p["construction_cargo_loss_upper_t"], "t"),
                    "construction_hull_loss_upper": (p["construction_hull_loss_upper"], "hull"),
                })
    water = by_key(study["water_catalogues"][f"fault_{mission}"], lambda p: p["id"])
    for case, p in selected_cases(study).items():
        w = water[p["water_id"]]
        base = baselines[p["mode"], p["construction_E_share"]]
        add("q3", case, p["id"], "joint_v9.json#water_catalogues,candidates,construction_baselines", {
            "gross_service_water_per_day": (w["gross_service_t_day"], "t/day"),
            "gross_service_water_over_horizon": (w["gross_service_t_day"] * w["water_horizon_days"], "t"),
            "water_service_horizon": (w["water_horizon_days"], "day"),
            "water_recovery_rate": (w["eta"], "fraction"),
            "initial_usable_water_on_moon": (w["initial_lunar_water_t"], "t"),
            "initial_packed_water_cargo": (w["initial_lunar_packed_t"], "t"),
            "fresh_water_reserve": (w["reserve_t"], "t"),
            "additional_preposition_upper": (p["additional_preposition_upper_days"], "day"),
            "incremental_central_budget_vs_matched_construction_only": (
                p["scenarios"]["central"]["cost_usd"] - base["scenarios"]["central"]["cost_usd"], "USD"),
        })
        add("q5", case, p["id"], "joint_v9.json#candidates,selections,cost_time_frontier_ids", {
            "elevator_construction_share": (p["construction_E_share"], "fraction"),
            "elevator_preposition_share": (p["preposition_E_share"], "fraction"),
            "habitation_upper": (p["habitation_upper_days"] / 365, "year"),
            "central_complete_policy_budget": (p["scenarios"]["central"]["cost_usd"], "USD"),
            "central_emissions_proxy": (p["scenarios"]["central"]["CO2proxy_kg"], "kg CO2 proxy"),
        })
    for index, row in enumerate(study["selections"]["central"]["epsilon_rows"]):
        if row["feasible"]:
            add("q4", f"central_emissions_cap_{index}", row["selected_policy_id"],
                "joint_v9.json#selections.central.epsilon_rows", {
                    "emissions_proxy_cap": (row["emissions_budget_kg"], "kg CO2 proxy"),
                    "selected_emissions_proxy": (row["CO2proxy_kg"], "kg CO2 proxy"),
                    "selected_central_budget": (row["cost_usd"], "USD"),
                })
    path = RESULTS / "论文组结果表.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-with", type=Path, help="directory of the original v9 archive")
    args = parser.parse_args()
    audit = read_json(RESULTS, "independent_v9.json")
    if audit.get("all_implemented_checks_pass") is not True:
        raise SystemExit("The v9 numerical verifier must pass before exporting paper results")
    study = read_json(RESULTS, "joint_v9.json")
    if args.compare_with:
        report = compare_archive(args.compare_with, study)
        (RESULTS / "archive_comparison.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(report, ensure_ascii=False))
    print(export_paper_data(study))


if __name__ == "__main__":
    main()
