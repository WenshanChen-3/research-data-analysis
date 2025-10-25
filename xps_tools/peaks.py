# this file is for background & area integration
from __future__ import annotations
from typing import Tuple, Literal
import numpy as np

def _slice_window(x: np.ndarray, y: np.ndarray, window: Tuple[float, float]):
    a, b = float(min(window)), float(max(window))
    m = (x >= a) & (x <= b)
    return x[m], y[m]

def baseline_linear(
    energy: np.ndarray,
    intensity: np.ndarray,
    window: Tuple[float, float],
) -> np.ndarray:
    """
    Linear baseline through the two window endpoints (end-point line).
    """
    xw, yw = _slice_window(energy, intensity, window)
    if xw.size < 2:
        return np.zeros_like(xw)
    # end-point values
    x1, x2 = xw[0], xw[-1]
    y1, y2 = yw[0], yw[-1]
    m = (y2 - y1) / (x2 - x1 + 1e-30)
    b = y1 - m * x1
    return m * xw + b

def baseline_shirley(
    energy: np.ndarray,
    intensity: np.ndarray,
    window: Tuple[float, float],
    max_iter: int = 200,
    tol: float = 1e-6,
) -> np.ndarray:
    """
    Minimal Shirley background (iterative).
    Reference idea: background equals scaled integral of (signal - background)
    between high-BE and the current point, anchored at the endpoints.
    Assumes decreasing BE -> increasing KE is not essential here; uses energy axis as-is.
    """
    xw, yw = _slice_window(energy, intensity, window)
    n = xw.size
    if n < 3:
        return baseline_linear(energy, intensity, window)

    y_low, y_high = float(yw[0]), float(yw[-1])

    bg = np.linspace(y_low, y_high, n)  # initial guess: linear
    for _ in range(max_iter):
        # cumulative integral of (y - bg) (trapezoid)
        s = np.cumsum(np.r_[0.0, 0.5 * ( (yw[1:] - bg[1:]) + (yw[:-1] - bg[:-1]) ) * (xw[1:] - xw[:-1])])
        # scale so bg endpoints match anchors
        S_total = float(s[-1]) if s[-1] != 0 else 1e-30
        new_bg = y_low + (y_high - y_low) * (s / S_total)
        if np.max(np.abs(new_bg - bg)) < tol:
            bg = new_bg
            break
        bg = new_bg
    return bg

def integrate_area(
    energy: np.ndarray,
    intensity: np.ndarray,
    window: Tuple[float, float],
    background: Literal["linear", "shirley", "none"] = "linear",
) -> float:
    """
    Background-subtracted peak area over the given energy window (trapezoid).
    """
    xw, yw = _slice_window(energy, intensity, window)
    if xw.size < 2:
        return 0.0
    if background == "none":
        bg = np.zeros_like(xw)
    elif background == "shirley":
        bg = baseline_shirley(energy, intensity, window)
    else:
        bg = baseline_linear(energy, intensity, window)

    y_corr = yw - bg
    return float(np.trapz(y_corr, xw))
