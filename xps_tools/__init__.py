from .parameters import AttenuationParams
from .attenuation import (
    intensity_overlayer,
    intensity_substrate,
    ratio_over_to_sub,
    fit_thickness_from_ratio,
    fit_thickness_from_multi_angle,
    estimate_thickness_from_areas,
)
from .io import load_spectrum
from .peaks import integrate_area, baseline_linear, baseline_shirley
