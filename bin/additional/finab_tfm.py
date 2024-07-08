from numpy import loadtxt
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_plot_size, set_width, tex_fonts


plt.rcParams.update(tex_fonts)
fig, ax = plt.subplots(1, 1, figsize=set_plot_size(set_width('tfm')))


n_isotopes = [6, 13, 18]
runs_start = 'Example_He_burning_'

width = 0.8


n = n_isotopes[0]
A, X = loadtxt(f'runs/{runs_start}{n}/finab.dat',
               unpack=True, usecols=[0, 4])
A = A - 0.4
plt.bar(A, X, width=width, label=n)

n = n_isotopes[1]
A, X = loadtxt(f'runs/{runs_start}{n}/finab.dat',
               unpack=True, usecols=[0, 4])
A = A + 0.4
plt.bar(A, X, width=width, label=n)

n = n_isotopes[2]
A, X = loadtxt(f'runs/{runs_start}{n}/finab.dat',
               unpack=True, usecols=[0, 4])
ticks = []
tant = -1
for t in A:
    if t - 1 != tant:
        tant = t
        ticks.append(t)

plt.xticks(ticks)
plt.bar(A, X, width=width, label=n)


plt.yscale('log')
plt.ylim([1e-15, 1])
plt.legend(title='\# isotopes')
plt.grid()
plt.ylabel('Abundance')
plt.xlabel('Mass number A')
plt.title('He burning')
plt.savefig('runs/He_burning_finab.pdf', bbox_inches='tight')
plt.show()

