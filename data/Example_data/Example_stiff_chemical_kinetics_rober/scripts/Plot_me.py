from numpy import loadtxt
import matplotlib.pyplot as plt
import sys
sys.path.append('../../bin')
from xtfc_generalize import plot


net_size = 3


fig, ax = plt.subplots(net_size, 1, sharex=True, figsize=(5, 9))

data = loadtxt('tracked_nuclei.dat')
plt.subplots_adjust(hspace=0.1)

for i in range(net_size):
    ax[i].plot(data[:, 0], data[:, i + 1], marker='.')

plt.xscale('log')

plt.savefig('rober.jpg')
plt.show()


plot(n=5, n_neurons=3, net_size=net_size, y0=[1, 0, 0])

