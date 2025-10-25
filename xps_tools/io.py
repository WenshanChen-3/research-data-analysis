# this file is to load your raw data (either in .csv or .txt form robustly)
from __future__ import annotations
from typing import Optional, Tuple
import numpy as np
import pandas as pd

COMMON_ENERGY_NAMES = {
    "BE", "Binding Energy", "BindingEnergy", "binding_energy",
    "Energy", "E", "Kinetic Energy", "KineticEnergy", "KE"
}
COMMON_INTENSITY_NAMES = {
    "I", "Intensity", "Counts", "cps", "CPS", "Signal", "Y"
}

def _infer_columns(df: pd.DataFrame) -> Tuple[str, str]:
    cols = {c.strip(): c for c in df.columns}
    # try exact/common names
    for e in COMMON_ENERGY_NAMES:
        if e in cols:
            e_col = cols[e]; break
    else:
        # fallback to first numeric column
        e_col = next((c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])), df.columns[0])

    for i in COMMON_INTENSITY_NAMES:
        if i in cols:
            i_col = cols[i]; break
    else:
        # pick the next numeric column different from energy
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        i_col = next((c for c in numeric_cols if c != e_col), numeric_cols[-1])

    return e_col, i_col

def load_spectrum(
    path: str,
    energy_col: Optional[str] = None,
    intensity_col: Optional[str] = None,
    skiprows: int = 0,
    sep: Optional[str] = None,
    decimal: Optional[str] = None,
) -> Tuple[np.ndarray, np.ndarray]:

    """
    Load a spectrum from CSV/TXT with auto separator & header inference.
    Returns (energy, intensity) as ascending energy arrays.
    """

    df = pd.read_csv(path, sep=None, engine="python", skiprows=skiprows)
    if energy_col is None or intensity_col is None:
        e_col, i_col = _infer_columns(df)
    else:
        e_col, i_col = energy_col, intensity_col

    energy = np.asarray(df[e_col].to_numpy(dtype=float))
    intensity = np.asarray(df[i_col].to_numpy(dtype=float))

    # energy be sorted from low to high for consistent windowing
    order = np.argsort(energy)
    return energy[order], intensity[order]
