"""Render report figures from the verified v9 results."""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from construction_v9 import ConstructionInputs
from programming_handoff import ROOT, RESULTS, default_fault_policies, read_json, selected_cases
from utils.plot_style import PALETTE, apply_publication_style, export_figure


def axes(title, height=2.75):
    fig, ax = plt.subplots(figsize=(6.3, height), layout="constrained")
    ax.set_title(title, fontweight="bold", pad=8)
    return fig, ax


def save(fig, name):
    export_figure(fig, ROOT / "figures" / name, dpi=300, grayscale_preview=True)
    plt.close(fig)


def construction_bounds(study):
    mission = study["default_mission_key"]
    baselines = {(p["mode"], p["construction_E_share"]): p for p in study["construction_baselines"]
                 if p["mission_key"] == mission}
    fig, ax = axes("Construction delivery bounds")
    for index, share in enumerate((0.0, 0.30, 1.0)):
        ideal = baselines["ideal", share]["generic_construction_delivery_upper_days"] / 365
        fault = baselines["fault", share]["generic_construction_delivery_upper_days"] / 365
        ax.plot((ideal, fault), (index, index), color="#A7B0BA", linewidth=1.7, zorder=1)
        ax.scatter(ideal, index, marker="o", facecolors="white", edgecolors=PALETTE["primary"],
                   s=35, zorder=3, label="Ideal operation" if index == 0 else None)
        ax.scatter(fault, index, marker="s", color=PALETTE["contrast"],
                   s=29, zorder=3, label="Declared faults" if index == 0 else None)
        for value, direction in ((ideal, -1), (fault, 1)):
            ax.annotate(f"{value:,.0f}", (value, index), xytext=(7 * direction, 0),
                        textcoords="offset points", ha="right" if direction < 0 else "left", va="center")
    ax.set(xlabel="Delivery upper bound (years)", xlim=(0, 1190), ylim=(2.55, -0.55),
           yticks=range(3), yticklabels=("Ground rockets", "Mixed, 30% elevator", "Elevator chain"))
    ax.legend(loc="upper right", ncols=2)
    save(fig, "result_q1_construction_bounds")


def fault_budgets():
    p = ConstructionInputs()
    fig, ax = axes("Construction fault inputs")
    labels = ("Elevator lift", "Apex dispatch", "Ground launch site", "Lunar receiving port")
    days = (p.lift_closed_days, p.E_closed_days, p.R_closed_days, p.port_closed_days)
    bars = ax.barh(labels, days, height=0.52, color=PALETTE["primary"])
    ax.bar_label(bars, labels=[str(x) for x in days], padding=4)
    ax.set(xlabel="Allowed additional closures (days per 365 days)", xlim=(0, 68))
    ax.invert_yaxis()
    save(fig, "raw_q2_declared_fault_budgets")


def water_preposition(study):
    cases = selected_cases(study)
    phases = read_json(RESULTS, "phases_v9.json")["phases"]
    groups = [[], [], []]
    for p in cases.values():
        stages = [phases[key] for key in p["phase_ids"][1:]]
        spans = (
            sum(s["duration_upper_days"] for s in stages if s.get("item_kind")),
            sum(s["duration_upper_days"] for s in stages if s.get("label") == "initial_usable_water"),
            sum(s["duration_upper_days"] for s in stages if s["kind"] == "apex_water_staging"),
        )
        if not math.isclose(sum(spans), p["additional_preposition_upper_days"], abs_tol=1e-7):
            raise ValueError(f"Unaccounted preposition duration for {p['id']}")
        for group, span in zip(groups, spans):
            group.append(span)

    fig, ax = axes("Water service preparation", height=2.9)
    positions = range(3)
    labels = ("Lowest central budget", "Earliest habitation bound", "Stock only, lowest budget")
    left = [0.] * 3
    for widths, label, color, hatch in zip(
        groups, ("Equipment", "Initial usable water", "Apex operating stock"),
        (PALETTE["primary"], PALETTE["sky"], PALETTE["secondary"]), ("", "//", "xx"),
    ):
        ax.barh(positions, widths, height=0.48, left=left, label=label, color=color,
                edgecolor="#333333", linewidth=0.55, hatch=hatch)
        left = [a + b for a, b in zip(left, widths)]
    for index, duration in enumerate(left):
        ax.annotate(f"{duration:,.0f}", (duration, index), xytext=(5, 0),
                    textcoords="offset points", va="center")
    ax.set(xlim=(0, 3370), ylim=(2.55, -0.75), yticks=positions, yticklabels=labels,
           xlabel="Additional preposition upper bound (days)")
    ax.legend(loc="upper right", ncols=3)
    save(fig, "process_q3_water_preposition")


def tradeoffs(study):
    policies = default_fault_policies(study)
    scenarios = study["selections"]["central"]

    def metrics(row, x):
        return x(row), row["scenarios"]["central"]["cost_usd"] / 1e12

    def panel(title, x_label, x, ids):
        fig, ax = axes(title, height=3.1)
        coordinates = [metrics(p, x) for p in policies]
        ax.scatter(*zip(*coordinates), s=7, color="#65798D", alpha=0.26,
                   linewidths=0, label="Candidate policies")
        frontier = sorted({metrics(p, x) for p in policies if p["id"] in ids})
        ax.step(*zip(*frontier), where="post", color=PALETTE["primary"], linewidth=1.65,
                label="Nondominated frontier")
        ax.set(xlabel=x_label, ylabel="Central budget (trillion USD)")
        ax.legend(loc="upper right")
        return fig, ax

    fig, _ = panel("Budget and emissions proxy", "Modeled emissions proxy (billion t CO2)",
                   lambda row: row["scenarios"]["central"]["CO2proxy_kg"] / 1e12,
                   set(scenarios["cost_environment_frontier_ids"]))
    save(fig, "result_q4_emissions_budget_frontier")

    x = lambda row: row["habitation_upper_days"] / 365
    fig, ax = panel("Budget and habitation time", "Habitation upper bound (years)", x,
                    set(study["cost_time_frontier_ids"]))
    selected = selected_cases(study)
    for key, label, marker in (
        ("earliest_habitation_bound", "Earliest bound", "D"),
        ("minimum_central_budget", "Lowest budget", "^"),
    ):
        point = metrics(selected[key], x)
        ax.scatter(*point, s=36, color=PALETTE["contrast"], edgecolors="white", marker=marker,
                   zorder=4, label=label)
    ax.legend(loc="upper right")
    save(fig, "result_q5_habitation_budget_frontier")


def main():
    study = read_json(RESULTS, "joint_v9.json")
    if read_json(RESULTS, "independent_v9.json").get("all_implemented_checks_pass") is not True:
        raise SystemExit("Run the v9 numerical verifier before plotting")
    apply_publication_style(language="en")
    plt.rcParams.update({"font.size": 9, "axes.titlesize": 11, "axes.labelsize": 9,
                         "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.8})
    construction_bounds(study)
    fault_budgets()
    water_preposition(study)
    tradeoffs(study)


if __name__ == "__main__":
    main()
