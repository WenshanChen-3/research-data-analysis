import math
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from xps_tools import AttenuationParams, fit_thickness_from_ratio
from xps_tools.plotting import plot_ratio_vs_thickness
from xps_tools.attenuation import ratio_over_to_sub


p = AttenuationParams(S_over=1.0, n_over=1.0, lam_over=2.0,
                      S_sub=1.0,  n_sub=1.0,  lam_sub_in_over=2.0)
theta = 0.0
R_meas = 1.54

info_depth = 3.0 * p.lam_sub_in_over * math.cos(math.radians(theta))  # ~6 nm here
d_max_plot = max(10.0, info_depth)  # show a bit more than the info depth

fit = fit_thickness_from_ratio(R_meas, theta, p, d0=2.0, bounds=(0.0, 50.0))
d_fit = fit["d"]

ax = plot_ratio_vs_thickness(R_meas, theta, p, d_range=(0.0, d_max_plot), fitted_d=d_fit)
ax.axvspan(info_depth, d_max_plot, alpha=0.15, hatch="//", color="firebrick", label="low sensitivity (>~3λcosθ)")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, frameon=True)

axins = inset_axes(ax, width="15%", height="25%", loc="center", borderpad=1)
plot_ratio_vs_thickness(R_meas, theta, p, d_range=(0.0, d_max_plot), fitted_d=d_fit, ax=axins)
axins.set_xlim(0.0, min(3.0, d_max_plot))
axins.set_ylim(0.0, 3.0)
axins.set_xticks([])
axins.set_yticks([])
axins.set_xticklabels([])
axins.set_yticklabels([])
axins.set_xlabel("")
axins.set_ylabel("")
axins.set_title("")
if axins.get_legend():
    axins.get_legend().remove()

mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", lw=1, ls="--", color="grey")

plt.tight_layout()
plt.show()