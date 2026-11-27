"""Axes-level plots for model diagnostics and decision evaluation."""

import numpy as np

THEME = {
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.alpha": 0.22,
    "figure.dpi": 150,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
}


def forecast_plot(ax, time, observed, forecast, lower, upper, unit):
    ax.fill_between(time, lower, upper, color="#137D78", alpha=0.20, label="90% prediction interval")
    ax.plot(time, observed, color="#26364D", linewidth=1, label="Observed")
    ax.plot(time, forecast, color="#137D78", linewidth=1, linestyle="--", label="Forecast")
    ax.set(xlabel="Time index", ylabel=f"Response ({unit})")
    ax.legend(frameon=False, ncols=2)


def residual_plot(ax, fitted, observed, unit):
    ax.scatter(fitted, np.asarray(observed) - fitted, s=10, alpha=0.6, color="#137D78")
    ax.axhline(0, color="#26364D", linewidth=1)
    ax.set(xlabel=f"Fitted value ({unit})", ylabel=f"Residual ({unit})")


def sensitivity_plot(ax, levels, cost, labels):
    colors = ["#26364D", "#137D78", "#B55726"]
    for series, label, color in zip(cost, labels, colors, strict=True):
        ax.plot(levels, series, marker="o", label=label, color=color)
    ax.set(xlabel="Shortage cost (currency/unit)", ylabel="Mean cost (currency)")
    ax.legend(frameon=False)
