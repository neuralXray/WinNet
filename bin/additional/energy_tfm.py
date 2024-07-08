from numpy import loadtxt
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_plot_size, set_width, tex_fonts


plt.rcParams.update(tex_fonts)
fig, ax = plt.subplots(1, 1, figsize=set_plot_size(set_width('tfm')))


n_isotopes = [6, 13, 18]
runs_start = 'Example_He_burning_'
for n in n_isotopes[:-1]:
    time_energy, energy = loadtxt(f'runs/{runs_start}{n}/generated_energy.dat',
                                  unpack=True, usecols=[0, 1])
    plt.plot(time_energy, energy, label=n)
n = n_isotopes[-1]
time_energy, energy = loadtxt(f'runs/{runs_start}{n}/generated_energy.dat',
                              unpack=True, usecols=[0, 1])
plt.plot(time_energy, energy, label=n, linestyle='dashed')

plt.xscale('log')
plt.yscale('log')
plt.xlabel("Time [s]")
plt.ylabel('Energy [erg g$^{-1}$ s$^{-1}$]')
plt.legend(title='\# isotopes')
plt.xlim([1e-12, 1e4])
plt.ylim([1e8, 1e26])
plt.grid()
plt.title('He burning')
plt.savefig('runs/He_burning_energy.pdf', bbox_inches='tight')
plt.show()

