from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AttenuationParams:
    """
    Parameters for a single overlayer on a semi-infinite substrate.

    All IMFPs are in nm, angles given to model functions are in degrees.
    S_* are sensitivity factors (or effective cross-sections),
    n_* are (relative) number densities or proportional factors.
    """
    S_over: float
    n_over: float
    lam_over: float
    S_sub: float
    n_sub: float
    lam_sub_in_over: float
    I0_over: float = 1.0
    I0_sub: float = 1.0
