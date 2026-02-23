# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:11:16 2025

@author: ksarg
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def _line_intersects_axes(line, xlim, ylim):
    """Return True if any point of the Line2D lies within the axis box (or touches it)."""
    try:
        x = np.asarray(line.get_xdata())
        y = np.asarray(line.get_ydata())
    except Exception:
        return False
    if x.size == 0 or y.size == 0:
        return False
    return (np.nanmin(x) <= xlim[1]) and (np.nanmax(x) >= xlim[0]) and \
           (np.nanmin(y) <= ylim[1]) and (np.nanmax(y) >= ylim[0])

def update_legend_filtered(ax, color_line_handles, color_line_labels,
                           separator1, separator2, style_handles,
                           loc="center left", bbox_to_anchor=(1, 0.5), fontsize=20):
    """
    Build a legend that contains:
      - separator1
      - only those color_line_handles whose data intersects current x/y limits (with color_line_labels)
      - separator2
      - the provided style_handles (e.g. electron linestyle custom handles)
    """
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    visible_handles = []
    visible_labels = []
    for h, lab in zip(color_line_handles, color_line_labels):
        if _line_intersects_axes(h, xlim, ylim):
            visible_handles.append(h)
            visible_labels.append(lab)

    # Combine handles/labels with separators and style handles
    handles = [separator1] + visible_handles + [separator2] + style_handles
    labels  = [separator1.get_label()] + visible_labels + [separator2.get_label()] + [h.get_label() for h in style_handles]

    # Replace the legend
    if handles:
        ax.legend(handles, labels, loc=loc, bbox_to_anchor=bbox_to_anchor, fontsize=fontsize)
    else:
        ax.legend([], [], loc=loc, bbox_to_anchor=bbox_to_anchor, fontsize=fontsize)

s = 3 #spin 9/2
m = 3 # m=1 transition

folder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Mathematica/"  # Use the same folder or use /parametersforplots/

# electron down degens
filename1down = f"{folder}constants_s{s}_m{m}_e1.csv"
constantsdown = np.loadtxt(filename1down, delimiter=",")

filename2down = f"{folder}labels_s{s}_m{m}_e1.csv"
labelsdown = np.loadtxt(filename2down, delimiter=",")

# electron up degens
filename1up = f"{folder}constants_s{s}_m{m}_e0.csv"
constantsup = np.loadtxt(filename1up, delimiter=",")

filename2up = f"{folder}labels_s{s}_m{m}_e0.csv"
labelsup = np.loadtxt(filename2up, delimiter=",")

numdegens = int(np.size(constantsup)/2)

plotsize_x = [-4, 4]
plotsize_y = [-4, 4]

x_min, x_max = plotsize_x[0], plotsize_x[1]
y_min, y_max = plotsize_y[0], plotsize_y[1]
y = np.linspace(y_min, y_max, 400)

fig, ax = plt.subplots(figsize=(6, 6))

# colours (keeps same cycle for later plots too)
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# We'll collect ONE plotted Line2D per nuclear-label to use for the filtered legend
color_line_handles = []
color_line_labels  = []

# Plot every pair and capture handles
for i in range(numdegens):
    if numdegens > 1:
        c1down = constantsdown[i][0]; c2down = constantsdown[i][1]
        c1up   = constantsup[i][0];   c2up   = constantsup[i][1]

        l1down = int(labelsdown[i][0]); l2down = int(labelsdown[i][1])
        l1up   = int(labelsup[i][0]);   l2up   = int(labelsup[i][1])
    else:
        c1down = constantsdown[0]; c2down = constantsdown[1]
        c1up   = constantsup[0];   c2up   = constantsup[1]

        l1down = int(labelsdown[0]); l2down = int(labelsdown[1])
        l1up   = int(labelsup[0]);   l2up   = int(labelsup[1])

    xdown = c1down * y + c2down
    xup   = c1up   * y + c2up

    h_down = ax.plot(xdown, y, linestyle='--', lw=5, color=colors[i])[0]
    h_up   = ax.plot(xup,   y, linestyle=':',  lw=5, color=colors[i])[0]

    # Create the nuclear label (one per unique pair) and remember one handle for the legend
    label = rf"$|{l1up}/2\rangle, |{l2up}/2\rangle$"
    if label not in color_line_labels:
        color_line_handles.append(h_down)   # store a representative plotted Line2D
        color_line_labels.append(label)

# Create separators and electron-style handles (kept always in legend)
separator1 = Line2D([0], [0], color='white', lw=0, label="nucleus")
separator2 = Line2D([0], [0], color='white', lw=0, label="electron")

line_handles = [
    Line2D([0], [0], linestyle='--', color='black', lw=5, label=r"$|\downarrow\rangle$"),
    Line2D([0], [0], linestyle=':',  color='black', lw=5, label=r"$|\uparrow\rangle$")
]

# Axis limits / ticks / labels (explicit)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks(np.linspace(x_min, x_max, 5))
ax.set_yticks(np.linspace(y_min, y_max, 5))

ax.set_xlabel(r"$\frac{a_i}{\omega_i}$", fontsize=25)
ax.set_ylabel(r"$\frac{\Delta_{\mathrm{Q},i}}{\omega_i}$", fontsize=25)
ax.set_title(rf"$ \Delta m={m} $", fontsize=25)
ax.tick_params(axis='both', which='major', labelsize=25)

# Build the filtered legend now
update_legend_filtered(ax,
                       color_line_handles, color_line_labels,
                       separator1, separator2, line_handles,
                       loc="center left", bbox_to_anchor=(1, 0.5), fontsize=20)

# OPTIONAL: update legend automatically on pan/zoom (interactive backends)
def _on_xlim_ylim_change(ax):
    update_legend_filtered(ax,
                           color_line_handles, color_line_labels,
                           separator1, separator2, line_handles,
                           loc="center left", bbox_to_anchor=(1, 0.5), fontsize=20)

# Connect callbacks (these will fire when xlim/ylim change interactively)
ax.callbacks.connect('xlim_changed', _on_xlim_ylim_change)
ax.callbacks.connect('ylim_changed', _on_xlim_ylim_change)

# Save & show
#outputfolder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Python/"
outputfolder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/2. Onetangles Project/Fig9 SVGs/"
plt.savefig(f"{outputfolder}degeneracyplot_s{s}_m{m}.svg", dpi=300, bbox_inches='tight')
plt.show()



# Create s+1 equally spaced levels from +9/2 to -9/2
levels = np.linspace(s, -s, s+1)
levellabels = [int(levels[i]) for i in range(s)]
plt.figure(figsize=(6, 8))

# Plot horizontal black lines with labels at the right
for level in levels:
    plt.hlines(level, 0, 1, colors='black', linewidth=5)
    # Format the label so that whole numbers appear as integers
    plt.text(1.05, level, rf"$|{int(level) if level.is_integer() else level:.0f}/2\rangle$", 
             fontsize=25, verticalalignment='center')


# Determine the number of arrows (one arrow per allowed transition)
num_arrows = s + 1 - m  # For example, if s=9 and m=7, then num_arrows = 10-7 = 3

x_positions = [(i+1)/(num_arrows+1) for i in range(num_arrows)]

# Get the same color cycle as used in the first (line-plot) code
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Draw vertical double-headed arrows.
# Each arrow connects the level at index i to the level at index i+m,
# and its color is taken from the colors list.
for i in range(num_arrows):
    y_start = levels[i]      # Upper level of the arrow
    y_end = levels[i + m]    # Lower level of the arrow
    x = x_positions[i]
    plt.annotate(
        "", 
        xy=(x, y_end), 
        xytext=(x, y_start),
        arrowprops=dict(arrowstyle="<|-|>", color=colors[i], linewidth=5)
    )

# Formatting the figure
plt.xticks([])
plt.yticks([])
plt.ylim(levels[-1] - 0.5, levels[0] + 0.5)
plt.xlim(-0.1, 1.2)
plt.box(False)
#plt.title(f"Transitions for m={m}")

plt.savefig(f"{outputfolder}transitions_s{s}_m{m}.svg", dpi=300, bbox_inches='tight')
plt.show()





