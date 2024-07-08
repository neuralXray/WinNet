# Author: M. Reichert
# Date: 09.07.22
import numpy as np
import matplotlib.pyplot as plt
# Import the WinNet python plot-routine
# Note that you can also just append the path to your .bashrc
import sys
sys.path.append('../../bin')
from class_files.winnet_class import winnet
import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_plot_size, set_width, tex_fonts


# This script will plot the mass fractions and energy generation
# of He burning. The plot can be compared to the one on cococubed:
# https://cococubed.com/code_pages/burn_helium.shtml

# Set up the figure
plt.rcParams.update(tex_fonts)
fig, ax = plt.subplots(1, 1, figsize=set_plot_size(set_width('tfm')))
ax.set_title('He burning with 6 isotopes')


def create_nucleus_name(s):
    '''
      Function to convert the element string that is given by WinNet
      to a latex style string.
      Example:
        create_nucleus_name('ne20')
      will output: r'$^{20}$Ne'
    '''
    digits =''
    chars  =''
    for d in s:
        if d.isdigit():
            chars = chars[0].upper() + chars[1:]
            digits+=d
        else:
            chars+=d
    nuc_name = r'$^{'+digits+'}$'+chars
    return nuc_name

# Read the mass fractions of the elements
w = winnet('.')
w.read_tracked_nuclei()
names = w.get_tracked_nuclei_names()
time  = w.get_tracked_time()

# Define the x-position of each element label
xpos_dic = {'he4':1e2,'c12':1e3,'o16':1e2,'ne20':5e0,\
            'mg24':5e2,'si28':2e-12,}

for n in names:
    # Plot the mass fractions of each element
    X = w.get_tracked_nuclei(n)
    line, = ax.plot(time,X,linewidth=1)
    # Plot the element labels
    if n in xpos_dic:
        out_name = create_nucleus_name(n)
        idx = np.argmin(abs(time-xpos_dic[n]))
        ax.text(xpos_dic[n],X[idx],out_name,ha='left',va='bottom',color=line.get_color())

# Plot also the generated energy on a second y-axis
ax_energy = ax.twinx()
time_energy,energy = np.loadtxt('generated_energy.dat',unpack=True,usecols=[0,1])
ax_energy.plot(time_energy,energy,ls='--',lw=1,color='saddlebrown',zorder=-30,alpha=0.8)
ax_energy.text(1e-11,1e24,r'$\epsilon$',color='saddlebrown')
ax_energy.set_yscale('log')
ax_energy.set_ylabel(r'Energy [erg g$^{-1}$ s$^{-1}$]')
ax_energy.set_ylim(1e8,1e26)

# Set the labels, limits, and scales
ax.set_xlabel('Time [s]')
ax.set_ylabel('Mass fraction')
ax.loglog()
ax.set_xlim(1e-12, 1e4)
ax.set_ylim(1e-18, 1e0)
ax.grid()
plt.savefig('He_burning_6.pdf', bbox_inches='tight')
plt.show()

