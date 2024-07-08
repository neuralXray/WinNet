from numpy import loadtxt
import matplotlib.pyplot as plt


# Prepare the plot
marker='.'
markersize=3
subplots = (3, 1)
fig, ax = plt.subplots(subplots[0], subplots[1], sharex=True, sharey=True)

data = loadtxt('runs/.Example_stiff_chemical_kinetics_belousovzhabotinsky/tracked_nuclei.dat')
ax[0].plot(data[:, 0], data[:, 2], marker=marker, markersize=markersize, lw=1, color='blue')
ax[0].plot(data[:, 0], data[:, 4], marker=marker, markersize=markersize, lw=1, color='red')
ax[0].plot(data[:, 0], data[:, 6], marker=marker, markersize=markersize, lw=1, color='orange')
ax[0].plot(data[:, 0], data[:, 7], marker=marker, markersize=markersize, lw=1, color='purple')
ax[0].legend(['Y', 'P', 'Z', 'Q'], loc='upper left')
ax[0].set_xlim([0, 40])
ax[0].set_ylabel('Abundance')
ax[0].set_ylim([0, 0.0055])
ax[0].grid()
ax[0].set_title('Adapting time step')
ax2 = ax[0].twinx()
ax2.set_ylim([0, 1.3e-5])
ax2.set_ylabel('Abundance')
ax2.plot(data[:, 0], data[:, 3], marker=marker, markersize=markersize, lw=1, color='green')
ax2.legend(['X'])


data = loadtxt('runs/.Example_stiff_chemical_kinetics_belousovzhabotinsky_lg/tracked_nuclei.dat')
ax[1].plot(data[:, 0], data[:, 2], marker=marker, markersize=markersize, lw=1, color='blue')
ax[1].plot(data[:, 0], data[:, 4], marker=marker, markersize=markersize, lw=1, color='red')
ax[1].plot(data[:, 0], data[:, 6], marker=marker, markersize=markersize, lw=1, color='orange')
ax[1].plot(data[:, 0], data[:, 7], marker=marker, markersize=markersize, lw=1, color='purple')
ax[1].legend(['Y', 'P', 'Z', 'Q'], loc='upper left')
ax[1].set_ylabel('Abundance')
ax[1].grid()
ax[1].set_title('Linear time grid with step 10$^{-3}$ s')
ax2 = ax[1].twinx()
ax2.set_ylim([0, 1.3e-5])
ax2.set_ylabel('Abundance')
ax2.plot(data[:, 0], data[:, 3], marker=marker, markersize=markersize, lw=1, color='green')
ax2.legend(['X'])


data = loadtxt('runs/.Example_stiff_chemical_kinetics_belousovzhabotinsky_lg1/tracked_nuclei.dat')
ax[2].plot(data[:, 0], data[:, 2], marker=marker, markersize=markersize, lw=1, color='blue')
ax[2].plot(data[:, 0], data[:, 4], marker=marker, markersize=markersize, lw=1, color='red')
ax[2].plot(data[:, 0], data[:, 6], marker=marker, markersize=markersize, lw=1, color='orange')
ax[2].plot(data[:, 0], data[:, 7], marker=marker, markersize=markersize, lw=1, color='purple')
ax[2].set_xlabel('Time [s]')
ax[2].legend(['Y', 'P', 'Z', 'Q'], loc='upper left')
ax[2].set_ylabel('Abundance')
ax[2].grid()
ax[2].set_title('Linear time grid with step 10$^{-2}$ s')
ax2 = ax[2].twinx()
ax2.plot(data[:, 0], data[:, 3], marker=marker, markersize=markersize, lw=1, color='green')
ax2.legend(['X'])
ax2.set_ylim([0, 1.3e-5])
ax2.set_ylabel('Abundance')


plt.savefig("runs/Belousov-Zhabotinsky.pdf",bbox_inches="tight")
plt.show()

