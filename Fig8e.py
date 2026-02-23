import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

"""
@author: Khadija Sarguroh (khadija.sarguroh@lmh.ox.ac.uk)
"""

# ----- params -----
s = 9
folder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Mathematica/" #Use the same folder or use /parametersforplots/
outputfolder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Python/"

# axes limits / ticks / labels
x_min, x_max = 0, 0.5
y_min, y_max = 0, 1
xticks = np.linspace(x_min, x_max, 6)
yticks = np.linspace(y_min, y_max, 5)

ms = list(range(1, 9))  # Δm panels: 1..8
palette = [plt.get_cmap("tab10")(i) for i in range(10)]  # high-contrast colours

# sizes
TITLE_FS  = 18
LABEL_FS  = 18
TICK_FS   = 18
LEGEND_FS = 18
LW        = 6

def _line_intersects_axes(line, xlim, ylim):
    try:
        x = np.asarray(line.get_xdata()); y = np.asarray(line.get_ydata())
    except Exception:
        return False
    if x.size == 0 or y.size == 0:
        return False
    return (np.nanmin(x) <= xlim[1]) and (np.nanmax(x) >= xlim[0]) and \
           (np.nanmin(y) <= ylim[1]) and (np.nanmax(y) >= ylim[0])

def plot_panel(ax, s, m):
    fn_const_down = f"{folder}constants_s{s}_m{m}_e1.csv"
    fn_const_up   = f"{folder}constants_s{s}_m{m}_e0.csv"
    fn_labels_up  = f"{folder}labels_s{s}_m{m}_e0.csv"

    constantsdown = np.loadtxt(fn_const_down, delimiter=",")
    constantsup   = np.loadtxt(fn_const_up,   delimiter=",")
    labelsup      = np.loadtxt(fn_labels_up,  delimiter=",")

    numdegens = int(np.size(constantsup) / 2)
    y = np.linspace(y_min, y_max, 400)

    pair_entries = []  # (h_down, h_up, label, color)

    for i in range(numdegens):
        if numdegens > 1:
            c1down, c2down = constantsdown[i][0], constantsdown[i][1]
            c1up,   c2up   = constantsup[i][0],   constantsup[i][1]
            l1up, l2up     = int(labelsup[i][0]), int(labelsup[i][1])
        else:
            c1down, c2down = constantsdown[0], constantsdown[1]
            c1up,   c2up   = constantsup[0],   constantsup[1]
            l1up, l2up     = int(labelsup[0]), int(labelsup[1])

        xdown = c1down * y + c2down
        xup   = c1up   * y + c2up

        color = palette[i % len(palette)]
        h_down = ax.plot(xdown, y, linestyle='--', lw=LW, color=color)[0]  # |↓⟩
        h_up   = ax.plot(xup,   y, linestyle=':',  lw=LW, color=color)[0]  # |↑⟩

        label = rf"$|{l1up}/2\rangle, |{l2up}/2\rangle$"
        pair_entries.append((h_down, h_up, label, color))

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.tick_params(axis='both', which='major', labelsize=TICK_FS)
    ax.set_title(rf"$\Delta m={m}$", fontsize=TITLE_FS)
    ax.set_box_aspect(1)  # TRUE square subplot box

    return pair_entries

# ---------- Figure: 4×2, tighter layout ----------
if __name__ == "__main__":
    fig, axes = plt.subplots(4, 2, figsize=(12, 18))  # no constrained_layout
    # Reduce whitespace between columns/rows and reserve a slimmer legend margin
    fig.subplots_adjust(wspace=0, hspace=0.2, right=0.7)

    # Label left-column y and bottom-row x
    for r in range(4):
        for c in range(2):
            ax = axes[r, c]
            if r != 3:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel(r"$\frac{\mathrm{a}_i}{\omega_i}$", fontsize=LABEL_FS)
            if c == 0:
                ax.set_ylabel(r"$\frac{\Delta_{\mathrm{Q},i}}{\omega_i}$", fontsize=LABEL_FS)
            else:
                ax.set_yticklabels([])

    # Plot and collect legend entries (visible-only)
    all_sections = []
    for ax, m in zip(axes.ravel(), ms):
        entries = plot_panel(ax, s=s, m=m)
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        visible_handles = []
        for h_down, h_up, label, color in entries:
            if _line_intersects_axes(h_down, xlim, ylim) or _line_intersects_axes(h_up, xlim, ylim):
                visible_handles.append(Line2D([0], [0], linestyle='--', lw=LW, color=color, label=label))
        all_sections.append((m, visible_handles))

    # ---------- Combined legend with bold headers, spacer, and indented Δm ----------
    handles, labels = [], []

    # Nuclear section header (bold)
    handles.append(Line2D([0], [0], color='white', lw=0,
                          label=r"$\mathbf{nucleus}$"))
    labels.append(r"$\mathbf{nucleus}$")
    for m, vis in all_sections:
        if not vis:
            continue
        # Indented Δm header
        handles.append(Line2D([0], [0], color='white', lw=0,
                              label=r"\ \ " + rf"$\Delta m={m}$"))
        labels.append(rf"$\Delta m={m}$")
        handles.extend(vis)
        labels.extend([h.get_label() for h in vis])

    # Spacer line (blank entry)
    handles.append(Line2D([0], [0], color='white', lw=0))
    labels.append("")

    # Electron section header (bold)
    handles.append(Line2D([0], [0], color='white', lw=0,
                          label=r"$\mathbf{electron}$"))
    labels.append(r"$\mathbf{electron}$")
    handles.extend([
        Line2D([0], [0], linestyle='--', color='black', lw=LW, label=r"$|\downarrow\rangle$"),
        Line2D([0], [0], linestyle=':',  color='black', lw=LW, label=r"$|\uparrow\rangle$")
    ])
    labels.extend([h.get_label() for h in handles[-2:]])

    fig.legend(
        handles, labels,
        loc="center left",
        bbox_to_anchor=(0.72, 0.5),
        fontsize=LEGEND_FS,
        frameon=True,
        borderaxespad=0.0,
        handlelength=2.4
    )

    fig.savefig(f"{outputfolder}degeneracy_grid_s{s}.png", dpi=300, bbox_inches='tight')
    plt.show()
