from __future__ import annotations
from typing import Sequence, Tuple, Dict
import math
import numpy as np
from scipy.optimize import least_squares
from .parameters import AttenuationParams


def _cos(theta_deg: float) -> float:
    c = math.cos(math.radians(float(theta_deg)))
    return 0.0 if c < 0.0 else c

# forward model
def intensity_overlayer(
    S_over: float, n_over: float, lam_over: float, theta_deg: float, d_over: float, I0_over: float = 1.0
) -> float:
    """
    I_over = I0_over * S_over * n_over * lam_over * cosθ * [1 - exp(-d / (lam_over * cosθ))]
    """
    c = _cos(theta_deg)
    if c == 0.0:
        return 0.0
    return I0_over * S_over * n_over * lam_over * c * (1.0 - math.exp(-d_over / (lam_over * c)))

def intensity_substrate(
    S_sub: float, n_sub: float, lam_sub_in_over: float, theta_deg: float, d_over: float, I0_sub: float = 1.0
) -> float:
    """
    I_sub = I0_sub * S_sub * n_sub * exp(-d / (lam_sub_in_over * cosθ))
    """
    c = _cos(theta_deg)
    if c == 0.0:
        return 0.0
    return I0_sub * S_sub * n_sub * math.exp(-d_over / (lam_sub_in_over * c))

def ratio_over_to_sub(
    d_over: float, theta_deg: float, *, S_over: float, n_over: float, lam_over: float,
    S_sub: float, n_sub: float, lam_sub_in_over: float, I0_over: float = 1.0, I0_sub: float = 1.0
) -> float:
    """
    R = I_over / I_sub  (finite-thickness overlayer on semi-infinite substrate)
    """
    I_over = intensity_overlayer(S_over, n_over, lam_over, theta_deg, d_over, I0_over)
    I_sub  = intensity_substrate(S_sub, n_sub, lam_sub_in_over, theta_deg, d_over, I0_sub)
    return np.inf if I_sub == 0 else I_over / I_sub

# inversion: thickness from ratio(s)
def fit_thickness_from_ratio(
    R_meas: float,
    theta_deg: float,
    p: AttenuationParams,
    d0: float = 2.0,
    bounds: Tuple[float, float] = (0.0, 50.0),
) -> Dict[str, float]:
    """
    Estimate thickness d (nm) from one measured ratio R = I_over/I_sub at angle theta_deg.
    """
    R_meas = float(R_meas)

    def resid(d_arr: np.ndarray) -> np.ndarray:
        d = float(d_arr[0])
        R = ratio_over_to_sub(
            d, theta_deg,
            S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
            S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
            I0_over=p.I0_over, I0_sub=p.I0_sub
        )
        return np.array([R - R_meas], dtype=float)

    res = least_squares(resid, x0=np.array([d0], dtype=float), bounds=bounds, method="trf")
    d_best = float(res.x[0])
    R_fit = float(ratio_over_to_sub(
        d_best, theta_deg,
        S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
        S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
        I0_over=p.I0_over, I0_sub=p.I0_sub
    ))
    return {"d": d_best, "R_fit": R_fit, "success": bool(res.success)}

def fit_thickness_from_multi_angle(
    angles_deg: Sequence[float],
    ratios_meas: Sequence[float],
    p: AttenuationParams,
    d0: float = 2.0,
    bounds: Tuple[float, float] = (0.0, 50.0),
    weights: Sequence[float] | None = None,
) -> Dict[str, float]:
    """
    Jointly fit one thickness d to measured ratios at multiple angles.
    weights: optional per-point weights (e.g., 1/sigma^2). If None, all equal.
    """
    if len(angles_deg) != len(ratios_meas):
        raise ValueError("angles_deg and ratios_meas must have the same length.")
    w = np.ones(len(ratios_meas), dtype=float) if weights is None else np.asarray(weights, dtype=float)

    def resid(d_arr: np.ndarray) -> np.ndarray:
        d = float(d_arr[0])
        out = []
        for th, Rm, wi in zip(angles_deg, ratios_meas, w):
            R = ratio_over_to_sub(
                d, th,
                S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
                S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
                I0_over=p.I0_over, I0_sub=p.I0_sub
            )
            out.append(wi * (R - Rm))
        return np.asarray(out, dtype=float)

    res = least_squares(resid, x0=np.array([d0], dtype=float), bounds=bounds, method="trf")
    d_best = float(res.x[0])
    ratios_fit = [
        float(ratio_over_to_sub(
            d_best, th,
            S_over=p.S_over, n_over=p.n_over, lam_over=p.lam_over,
            S_sub=p.S_sub, n_sub=p.n_sub, lam_sub_in_over=p.lam_sub_in_over,
            I0_over=p.I0_over, I0_sub=p.I0_sub
        )) for th in angles_deg
    ]
    return {"d": d_best, "ratios_fit": ratios_fit, "success": bool(res.success)}

def estimate_thickness_from_areas(
    A_over: float,
    A_sub: float,
    theta_deg: float,
    p: AttenuationParams,
    d0: float = 2.0,
    bounds: Tuple[float, float] = (0.0, 50.0),
) -> Dict[str, float]:
    """
    Convenience wrapper for single-angle fits:
      - computes R = A_over / A_sub,
      - returns thickness and model ratio.
    """
    if A_sub <= 0:
        raise ValueError("A_sub must be > 0 to compute a ratio.")
    R = float(A_over) / float(A_sub)
    out = fit_thickness_from_ratio(R, theta_deg, p, d0=d0, bounds=bounds)
    out.update({"R_meas": R})
    return out
