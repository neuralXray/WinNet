from numpy import loadtxt
import matplotlib.pyplot as plt


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
plt.legend(title='# isotopes')
plt.xlim([1e-12, 1e4])
plt.ylim([1e8, 1e26])
plt.grid()
plt.title('He burning')
plt.show()

