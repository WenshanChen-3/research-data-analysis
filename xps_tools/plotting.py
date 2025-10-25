from __future__ import annotations
from typing import Sequence, Tuple
import numpy as np
import matplotlib.pyplot as plt

from .parameters import AttenuationParams
from .attenuation import ratio_over_to_sub

def plot_ratio_vs_thickness(
    R_meas: float,
    theta_deg: float,
    p: AttenuationParams,
    d_range: Tuple[float, float] = (0.0, 20.0),
    num: int = 400,
    fitted_d: float | None = None,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """
    Plot model R(d) over a thickness range and overlay the measured R and (optional) fitted d.
    """
    if ax is None:
        fig, ax = plt.subplots()

    d_vals = np.linspace(d_range[0], d_range[1], num=num)
    R_vals = [
        ratio_over_to_sub(
            d, theta_deg,
            S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
            S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
            I0_over=p.I0_over, I0_sub=p.I0_sub
        ) for d in d_vals
    ]
    ax.plot(d_vals, R_vals, label="Model R(d)")
    ax.axhline(R_meas, linestyle="--", label=f"Measured R = {R_meas:.3g}")
    if fitted_d is not None:
        ax.axvline(fitted_d, linestyle=":", label=f"Fitted d = {fitted_d:.3g} nm")
    ax.set_xlabel("Thickness d (nm)")
    ax.set_ylabel("Ratio R = I_over / I_sub")
    ax.set_title(f"Single-angle fit (θ = {theta_deg:g}°)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax

def plot_ratio_vs_angle(
    angles_deg: Sequence[float],
    ratios_meas: Sequence[float],
    p: AttenuationParams,
    fitted_d: float,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """
    Plot measured R(θ) points and model R(θ) at the fitted thickness.
    """
    if ax is None:
        fig, ax = plt.subplots()

    angles_deg = np.asarray(angles_deg, dtype=float)
    ratios_meas = np.asarray(ratios_meas, dtype=float)

    # the measured one
    ax.scatter(angles_deg, ratios_meas, label="Measured R(θ)")

    # smooth model curve through angle
    th_grid = np.linspace(float(angles_deg.min()), float(angles_deg.max()), 300)
    R_model = [
        ratio_over_to_sub(
            d_over=fitted_d, theta_deg=th,
            S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
            S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
            I0_over=p.I0_over, I0_sub=p.I0_sub
        ) for th in th_grid
    ]
    ax.plot(th_grid, R_model, label=f"Model @ d = {fitted_d:.3g} nm")

    ax.set_xlabel("Take-off angle θ (deg)")
    ax.set_ylabel("Ratio R = I_over / I_sub")
    ax.set_title("Multi-angle fit")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax
