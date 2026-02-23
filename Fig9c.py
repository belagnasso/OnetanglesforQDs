#%matplotlib inline

"""
@author: Khadija Sarguroh (khadija.sarguroh@lmh.ox.ac.uk)
"""

"""

This script plots and analyzes trigonometric functions of θ ∈ [0, π], focusing
on the relationship between sin(2θ), cos²(θ), and the derived curve
f(θ) = |sin(2θ)| − cos²(θ). It highlights maxima, minima, and approximate zeros
of the red curve, with annotated positions on the plot, and saves the final
figure as an image file.

Core components:
    - Functions:
        sin(2θ)                  → blue curve
        cos²(θ)                  → green curve
        |sin(2θ)| − cos²(θ)      → red curve (main quantity of interest)

    - Analysis:
        * Max and min values of the red curve are located numerically.
        * Indices of maxima/minima are identified and marked with red circles.
        * Approximate zeros of the red curve are detected where
          | |sin(2θ)| − cos²(θ) | < 0.01, with spacing control to avoid duplicates.
        * θ-values at zeros are annotated on the plot in units of π.

    - Plot styling:
        * Font sizes globally set to 20 pt (axes, labels, ticks, legend).
        * Vertical dashed reference lines at 0, π/4, π/2, 3π/4, and π.
        * X-axis ticks labeled with symbolic multiples of π.
        * Y-axis ticks restricted to {1, 0.5, 0, −0.5, −1}.
        * Red markers indicate extrema and zeros.
        * Legend placed outside to the right of the plot.

    - Output:
        * Saves the figure to
          "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Python/thetaparameter.png"
          at 300 dpi with tight bounding box.
        * Displays the figure interactively.

Usage:
    1. Run the script directly; it generates the figure automatically.
    2. Adjust the tolerance (tol) for zero-detection accuracy if needed.
    3. Edit `outputfolder` to change where the PNG is saved.

Dependencies: numpy, matplotlib
"""


import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.size': 20,          # Base font size for everything
    'axes.titlesize': 20,     # Title font size
    'axes.labelsize': 20,     # X and Y label size
    'xtick.labelsize': 20,    # X tick label size
    'ytick.labelsize': 20,    # Y tick label size
    'legend.fontsize': 20,    # Legend font size
    'figure.titlesize': 20    # Figure title size
})


# x values
theta = np.linspace(0, np.pi, 1000)

# functions
sin2theta = np.sin(2 * theta)
costheta2 = np.cos(theta)**2
red_curve = np.abs(sin2theta) - costheta2

# Max and Min values of red curve
y_max = np.max(red_curve)
y_min = np.min(red_curve)
tol = 1e-6  # tolerance for float comparison

# Indices of all max and min points
idx_max = np.where(np.abs(red_curve - y_max) < tol)[0]
idx_min = np.where(np.abs(red_curve - y_min) < tol)[0]

theta_max = theta[idx_max]
y_max_vals = red_curve[idx_max]

theta_min = theta[idx_min]
y_min_vals = red_curve[idx_min]

# Zeros of red curve (where abs(sin(2θ)) ≈ cos²(θ))
diff = np.abs(red_curve)
idx_zero_raw = np.where(diff < 0.01)[0]

# Filter repeated points (spacing by 10 points)
idx_zero = []
for i in idx_zero_raw:
    if not idx_zero or i - idx_zero[-1] > 10:
        idx_zero.append(i)

theta_zero = theta[idx_zero]
y_zero = red_curve[idx_zero]

# Plot
plt.figure(figsize=(18, 6))
plt.plot(theta, sin2theta, label=r'$f(\theta)=\sin(2\theta)$', color='blue')
plt.plot(theta, costheta2, label=r'$f(\theta)=\cos^2(\theta)$', color='green')
plt.plot(theta, red_curve, label=r'$f(\theta)=|\sin(2\theta)| - \cos^2(\theta)$', color='red')

# Mark all maxima
plt.plot(theta_max, y_max_vals, 'ro', markersize=6)#, label='Max of red curve')
for t, y in zip(theta_max, y_max_vals):
    plt.annotate(rf"{t/np.pi:.2f}" + r"$\pi$", (t, y), textcoords="offset points", xytext=(-5, 10), ha='right')

# Mark all minima
plt.plot(theta_min, y_min_vals, 'ro', markersize=6)#, label='Min of red curve')
#for t, y in zip(theta_min, y_min_vals):
#    plt.annotate(rf"{t/np.pi:.2f}" + r"$\pi$", (t, y), textcoords="offset points", xytext=(-5, -15), ha='right')

# Zeros
plt.plot(theta_zero, y_zero, 'ro', markersize=6)#, label='Zeros of red curve')
for t, y in zip(theta_zero, y_zero):
    label = rf"{t/np.pi:.2f}" + r"$\pi$"
    plt.annotate(label, (t, y), textcoords="offset points", xytext=(0, 10), ha='center')

# Vertical reference lines
for x in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
    plt.axvline(x, color='gray', linestyle='--')

# X-ticks
xticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
xtick_labels = ['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$']
plt.xticks(xticks, xtick_labels)

# Y-ticks (only 1, 0.5, 0, -0.5, -1)
plt.yticks([1, 0.5, 0, -0.5, -1])

# Labels and styling
plt.xlabel(r'$\theta$')
plt.ylabel(r'$f(\theta)$')
#plt.title('Trigonometric Functions with Red Curve Markers')
plt.axhline(0, color='black', linewidth=0.5)
# Legend outside to the right
plt.legend(
    loc="best",        # Anchor to the left of the legend box
    bbox_to_anchor=(1.5, 0.5),  # Push legend to the right
    borderaxespad=0
)

plt.tight_layout()

plt.tight_layout()

# Save and show
#outputfolder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Python/"
outputfolder = C:/Users/mert4325/OneDrive - Nexus365/DPhil/2. Onetangles Project/Fig9 SVGs/"
plt.savefig(f"{outputfolder}thetaparameter.svg", dpi=300, bbox_inches='tight')
plt.show()

