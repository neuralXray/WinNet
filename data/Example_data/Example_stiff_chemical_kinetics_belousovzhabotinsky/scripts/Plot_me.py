from numpy import loadtxt
import matplotlib.pyplot as plt
import sys
sys.path.append('../../bin')
from xtfc_generalize import predict


fig, ax = plt.subplots(2, 4, sharex=True, figsize=(10, 5))

data = loadtxt('tracked_nuclei.dat')

ax[0, 0].plot(data[:, 0], data[:, 1], marker='.')
ax[0, 1].plot(data[:, 0], data[:, 2], marker='.')
ax[0, 2].plot(data[:, 0], data[:, 3], marker='.')
ax[1, 0].plot(data[:, 0], data[:, 4], marker='.')
ax[1, 1].plot(data[:, 0], data[:, 5], marker='.')
ax[1, 2].plot(data[:, 0], data[:, 6], marker='.')
ax[1, 3].plot(data[:, 0], data[:, 7], marker='.')
plt.savefig('belousovzhabotinsky1.jpg')

plt.figure()
plt.plot(data[:, 0], data[:, 2], marker='.', color='blue')
plt.plot(data[:, 0], data[:, 4], marker='.', color='red')
plt.plot(data[:, 0], data[:, 6], marker='.', color='orange')
plt.plot(data[:, 0], data[:, 7], marker='.', color='purple')
plt.legend(['Y', 'P', 'Z', 'Q'])
plt.xlabel('Time [s]')
plt.ylabel('Abundance [u$^{-1}$]')
plt.twinx()
plt.plot(data[:, 0], data[:, 3], marker='.', color='green')
plt.legend(['X'])
plt.grid()
plt.ylabel('Abundance [u$^{-1}$]')
plt.savefig('belousovzhabotinsky2.jpg')
plt.show()


n = 3
n_neurons = 2
net_size = 7
y0 = [0.66, 0, 0, 0, 0.66, 0.002, 0]

fig, ax = plt.subplots(2, 4, sharex=True, figsize=(10, 5))

time, times, ys, dys = predict(n, n_neurons, net_size, y0)

ax[0, 0].plot(times, ys[:, 0], marker='.')
ax[0, 1].plot(times, ys[:, 1], marker='.')
ax[0, 2].plot(times, ys[:, 2], marker='.')
ax[1, 0].plot(times, ys[:, 3], marker='.')
ax[1, 1].plot(times, ys[:, 4], marker='.')
ax[1, 2].plot(times, ys[:, 5], marker='.')
ax[1, 3].plot(times, ys[:, 6], marker='.')
plt.savefig('belousovzhabotinsky1g.jpg')

plt.figure()
plt.plot(times, ys[:, 1], marker='.', color='blue')
plt.plot(times, ys[:, 3], marker='.', color='red')
plt.plot(times, ys[:, 5], marker='.', color='orange')
plt.plot(times, ys[:, 6], marker='.', color='purple')
plt.legend(['Y', 'P', 'Z', 'Q'])
plt.xlabel('Time [s]')
plt.ylabel('Abundance [u$^{-1}$]')
plt.twinx()
plt.plot(times, ys[:, 2], marker='.', color='green')
plt.legend(['X'])
plt.grid()
plt.ylabel('Abundance [u$^{-1}$]')
plt.savefig('belousovzhabotinsky2g.jpg')
plt.show()

