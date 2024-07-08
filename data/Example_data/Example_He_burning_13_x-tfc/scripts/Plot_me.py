# Author: M. Reichert
# Date: 09.07.22
import numpy as np
import matplotlib.pyplot as plt
# Import the WinNet python plot-routine
# Note that you can also just append the path to your .bashrc
import sys
sys.path.append('../../bin')
from class_files.winnet_class import winnet

# This script will plot the mass fractions and energy generation
# of He burning. The plot can be compared to the one on cococubed:
# https://cococubed.com/code_pages/burn_helium.shtml

# Set up the figure
fig = plt.figure()
ax  = fig.gca()
ax.set_title("He burning with 13 isotopes")

# Read the mass fractions of the elements
w = winnet(".")
w.read_tracked_nuclei()
names = w.get_tracked_nuclei_names()
time  = w.get_tracked_time()

for n in names:
    # Plot the mass fractions of each element
    X = w.get_tracked_nuclei(n)
    line, = ax.plot(time,X,marker='.',label=n)

# Plot also the generated energy on a second y-axis
ax_energy = ax.twinx()
time_energy,energy = np.loadtxt("generated_energy.dat",unpack=True,usecols=[0,1])
ax_energy.plot(time_energy,energy,ls="--",lw=1,color="saddlebrown",zorder=-30,alpha=0.8,label="$\epsilon$")
ax_energy.set_yscale("log")
ax_energy.set_ylabel(r"Energy [erg g$^{-1}$ s$^{-1}$]")
ax_energy.set_ylim(1e11,1e26)

# Set the labels, limits, and scales
ax.set_xlabel("Time [s]")
ax.set_ylabel("Mass fraction")
ax.loglog()
ax.set_xlim(1e-12,1e4)
ax.set_ylim(1e-15,1)
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax_energy.get_legend_handles_labels()
ax.legend(lines2 + lines, labels2 + labels)
ax.grid()
plt.savefig("He_burning_13.pdf",bbox_inches="tight")
plt.show()
