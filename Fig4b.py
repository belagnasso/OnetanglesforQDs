# -*- coding: utf-8 -*-
"""
@author: Khadija Sarguroh (khadija.sarguroh@lmh.ox.ac.uk)
"""

import numpy as np
import matplotlib.pyplot as plt

s = 3 #spin 9/2
m1 = 1# m=1 transition
m2 = 2

folder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Mathematica/"  # Use the same folder or use /parametersforplots/

# electron down degens
filename1downm1 = f"{folder}constants_s{s}_m{m1}_e1.csv"
constantsdownm1 = np.loadtxt(filename1downm1, delimiter=",")

filename2downm1 = f"{folder}labels_s{s}_m{m1}_e1.csv"
labelsdownm1 = np.loadtxt(filename2downm1, delimiter=",")

# electron up degens
filename1upm1 = f"{folder}constants_s{s}_m{m1}_e0.csv"
constantsupm1 = np.loadtxt(filename1upm1, delimiter=",")

filename2upm1 = f"{folder}labels_s{s}_m{m1}_e0.csv"
labelsupm1 = np.loadtxt(filename2upm1, delimiter=",")
## m2
# electron down degens
filename1downm2 = f"{folder}constants_s{s}_m{m2}_e1.csv"
constantsdownm2 = np.loadtxt(filename1downm2, delimiter=",")

filename2downm2 = f"{folder}labels_s{s}_m{m2}_e1.csv"
labelsdownm2 = np.loadtxt(filename2downm2, delimiter=",")

# electron up degens
filename1upm2 = f"{folder}constants_s{s}_m{m2}_e0.csv"
constantsupm2 = np.loadtxt(filename1upm2, delimiter=",")

filename2upm2 = f"{folder}labels_s{s}_m{m2}_e0.csv"
labelsupm2 = np.loadtxt(filename2upm2, delimiter=",")

constantsup = np.concatenate((constantsupm1,constantsupm2),axis=0)
constantsdown = np.concatenate((constantsdownm1,constantsdownm2),axis=0)

labelsup = np.concatenate((labelsupm1,labelsupm2),axis=0)
labelsdown = np.concatenate((labelsdownm1,labelsdownm2),axis=0)

### Comment out if needing vertical lines
# Filter using only labelsup (assumes nuclear labels are same in both)
mask = ~(((labelsup[:, 0] == 1) & (labelsup[:, 1] == -1)) | 
         ((labelsup[:, 0] == -1) & (labelsup[:, 1] == 1)))
constantsup = constantsup[mask]
constantsdown = constantsdown[mask]
labelsup = labelsup[mask]
labelsdown = labelsdown[mask]


numdegens = int(np.size(constantsup)/2)

# Adjust the range as needed
plotsize = [0,2.5]

# Define parameter range for y
y = np.linspace(plotsize[0], plotsize[1], 400)  

# Create the plot
plt.figure(figsize=(6, 6))

# colors
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

### Comment out if needing vertical lines
import matplotlib.colors as mcolors
# Optionally remove orange from colormap (comment this out to bring it back)
colors = [c for c in colors if not mcolors.to_hex(c) == '#ff7f0e']  # #ff7f0e is matplotlib "tab:orange"

# Now create a new color map from remaining colors
# ? doesn't actually change anything - same as before removing orange
new_cmap = mcolors.ListedColormap(colors)

# Iterate over combinations of c1 and c2
for i in range(numdegens):
    number = i
    if numdegens>1:

            c1down = constantsdown[i][0]
            c2down = constantsdown[i][1]
            c1up = constantsup[i][0]
            c2up = constantsup[i][1]
    
            l1down = int(labelsdown[i][0])
            l2down = int(labelsdown[i][1]) 
            l1up = int(labelsup[i][0])
            l2up = int(labelsup[i][1])
    else:

            c1down = constantsdown[0]
            c2down = constantsdown[1]
            c1up = constantsup[0]
            c2up = constantsup[1]
    
            l1down = int(labelsdown[0])
            l2down = int(labelsdown[1]) 
            l1up = int(labelsup[0])
            l2up = int(labelsup[1]) 

    xdown = c1down * y + c2down  # Compute x for given c1 and c2
    xup = c1up * y + c2up
    
    plt.plot(xdown, y, linestyle = '--', lw=5, color = colors[i])#, label=rf"$|{l1down}/2 \rangle, |{l2down}/2 \rangle$", )  # Plot with label
    plt.plot(xup, y, linestyle = ':', lw=5, color = colors[i])  # Plot with label

# Plot lines
color_labels = {}
for i in range(numdegens):
    if numdegens>1:
        c1down, c2down = constantsdown[i]
        c1up, c2up = constantsup[i]
        l1down, l2down = int(labelsdown[i][0]), int(labelsdown[i][1])
        l1up, l2up = int(labelsup[i][0]), int(labelsup[i][1])
    
    else:
        c1down, c2down = constantsdown
        c1up, c2up = constantsup
        l1down, l2down = int(labelsdown[0]), int(labelsdown[1])
        l1up, l2up = int(labelsup[0]), int(labelsup[1])
    
    xdown = c1down * y + c2down
    xup = c1up * y + c2up

    label = rf"$|{l1up}/2\rangle, |{l2up}/2\rangle$"
    if label not in color_labels:
        color_labels[label] = colors[i]

    plt.plot(xdown, y, linestyle='--', linewidth = 5,color=colors[i])
    plt.plot(xup, y, linestyle=':',linewidth = 5,  color=colors[i])

# Create legend handles for colors
color_handles = [plt.Line2D([0], [0], color=color, lw=5, label=label) for label, color in color_labels.items()]

# Create legend handles for line styles
line_handles = [
    plt.Line2D([0], [0], linestyle='--', color='black', lw=5, label=r"$|\downarrow\rangle$"),
    plt.Line2D([0], [0], linestyle=':', color='black', lw=5, label=r"$|\uparrow\rangle$")
]

# Add "dummy" entries to act as section titles
separator1 = plt.Line2D([0], [0], color='white', lw=0, label="Nucleus")
separator2 = plt.Line2D([0], [0], color='white', lw=0, label="Electron")

# Combine everything in one legend
combined_handles = [separator1] + color_handles + [separator2] + line_handles
plt.legend(handles=combined_handles, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=20)
# Formatting
plt.axis('equal')
plt.xlim(plotsize[0],plotsize[1])
plt.ylim(plotsize[0],plotsize[1])
plt.xlabel(r"$\frac{|a_1|}{\omega_1}$", fontsize=25)
plt.ylabel(r"$\frac{\Delta_{Q,1}}{\omega_1}$", fontsize=25)

#plt.title(rf"$ m={m1},{m2} $", fontsize=25)
#plt.legend(loc="center left", bbox_to_anchor=(1, 0.5)) 
#plt.legend(handles=color_handles, title="Nuclear Degeneracies", loc="center left", bbox_to_anchor=(1, 0.5))
plt.xticks(np.linspace(plotsize[0], plotsize[1], 6))  # 6 nicely spaced ticks from 0 to 2.5
plt.yticks(np.linspace(plotsize[0], plotsize[1], 6))
plt.tick_params(axis='both', which='major', labelsize=25)  # Adjust number as needed


outputfolder = "C:/Users/mert4325/OneDrive - Nexus365/DPhil/Python/"
plt.savefig(f"{outputfolder}degeneracyplot_s{s}_m{m1},{m2}.svg", dpi=600, bbox_inches='tight')
#plt.legend()
plt.show()

# Create s+1 equally spaced levels from +9/2 to -9/2
levels = np.linspace(s, -s, s+1)
levellabels = [int(levels[i]) for i in range(s)]
plt.figure(figsize=(6, 8))

# Plot horizontal black lines with labels at the right
for level in levels:
    plt.hlines(level, 0, 1, colors='black', linewidth=2)
    # Format the label so that whole numbers appear as integers
    plt.text(1.05, level, rf"$|{int(level) if level.is_integer() else level:.0f}/2\rangle$", 
             fontsize=30, verticalalignment='center')


# Determine the number of arrows (one arrow per allowed transition)
num_arrows1 = s + 1 - m1
num_arrows2 = s + 1 - m2  # For example, if s=9 and m=7, then num_arrows = 10-7 = 3
num_arrows = num_arrows1 + num_arrows2

x_positions = [(i+1)/(num_arrows+1) for i in range(num_arrows)]

# Get the same color cycle as used in the first (line-plot) code
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Draw vertical double-headed arrows.
# Each arrow connects the level at index i to the level at index i+m,
# and its color is taken from the colors list.

for i in range(num_arrows):
    if i < num_arrows1:    
        y_end = levels[i + m1] # Lower level of the arrow
        y_start = levels[i] # Upper level of the arrow
    else:
        y_start = levels[i-num_arrows2] # Upper level of the arrow
        y_end = levels[i-num_arrows2 - m2]
    x = x_positions[i]
    
    plt.annotate(
        "", 
        xy=(x, y_end), 
        xytext=(x, y_start),
        arrowprops=dict(arrowstyle="<->", color=colors[i], linewidth=3)
    )

# Formatting the figure
plt.xticks([])
plt.yticks([])
plt.ylim(levels[-1] - 0.5, levels[0] + 0.5)
plt.xlim(-0.1, 1.2)
plt.box(False)
#plt.title(f"Transitions for m={m}")

plt.savefig(f"{outputfolder}transitions_s{s}_m{m1}{m2}.svg", dpi=300, bbox_inches='tight')
plt.show()





