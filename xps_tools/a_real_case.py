# here is a showcase from xps data in .csv file
from xps_tools import (
    load_spectrum, integrate_area,
    AttenuationParams, estimate_thickness_from_areas
)

# Load your raw spectrum (CSV or TXT) in the same folder
# the separator(, ; etc..) and columns are auto detected, however, you can overwrite if you need it
energy, intensity = load_spectrum(
    path="example.csv",
    sep=";",
    energy_col=None,
    intensity_col=None,
)

#This example is from an ultra-thin oxide layer grown on oxide substrate where O1s contributed from 2 layers being detected
OVER_WINDOW = (530.3, 535.5)   # O 1s film, BE unit in eV
SUB_WINDOW  = (528.5, 532.5)   # O 1s sub., BE unit in eV

# 1. If your XPS spectra are already background-subtracted (for example, processed in CasaXPS, Avantage, or another fitting program),set the background option to "none" when integrating peaks. This keeps the intensities exactly as exported and avoids double subtraction.
# 2. If you are working with raw spectra directly from the instrument, you can let the script perform background correction automatically
# 3. Personally I prefer subtraction the background in CasaXPS before moving forward
A_over = integrate_area(energy, intensity, OVER_WINDOW, background="none")
A_sub  = integrate_area(energy, intensity, SUB_WINDOW,  background="none")
print(f"A_over={A_over:.4f}, A_sub={A_sub:.4f}, R={A_over/A_sub if A_sub>0 else float('inf'):.4f}")

#Replace the attenuation parameters with your materials
p = AttenuationParams(
    S_over=1.0, n_over=1.0, lam_over=2.0,     # nm
    S_sub=1.0,  n_sub=1.0,  lam_sub_in_over=2,
)

# Fit thickness
theta = 0.0
fit = estimate_thickness_from_areas(A_over=A_over, A_sub=A_sub, theta_deg=theta, p=p, d0=2.0, bounds=(0.0, 50.0))
print(f"thickness (nm): {fit['d']:.3f}  |  R_meas={fit['R_meas']:.4f}  |  R_fit={fit['R_fit']:.4f}  |  success={fit['success']}")
