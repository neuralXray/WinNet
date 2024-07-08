# Author: M. Reichert
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_subplots_size, tex_fonts


# Prepare the plot
subplots = (2, 1)
plt.rcParams.update(tex_fonts)
fig, ax = plt.subplots(subplots[0], subplots[1], sharex=True,
                       figsize=set_subplots_size(width='tfm', fraction=1, subplots=subplots))


y_min = 1e-3
# REACLIB rates:
lambda_ni = np.exp(-0.135415e+02)
lambda_co = np.exp(-0.160997e+02)

def analyticSol(y0,t):
    y_ni0, y_co0, y_fe0 = [y0[0], y0[1], y0[2]]
    y_ni = y_ni0*np.exp(-lambda_ni*t)
    #degenerate case?
    if(lambda_ni==lambda_co):
        y_co = y_co0*np.exp(-lambda_ni*t) + lambda_ni*y_ni0*t*np.exp(-lambda_ni*t)
    else:
        y_co = y_co0*np.exp(-lambda_co*t) + (lambda_ni/(lambda_co - lambda_ni))*y_ni0*(np.exp(-lambda_ni*t) - np.exp(-lambda_co*t))
    y_fe = np.sum(y0) - y_ni - y_co
    return np.array([y_ni, y_co, y_fe])


# Plot analytic solution
y0 = np.array([1.0/56.0, 0.0, 0.0])
t_ana = [0]
step = 1e4
ti = step
t_f = 1e8
while ti < t_f:
    t_ana.append(ti)
    step = step * 1.2
    ti = ti + step

t_ana.append(t_f)
t_ana = np.array(t_ana)

y_ana = analyticSol(y0, t_ana)
ax[0].plot(t_ana, y_ana[0]*56, color='k',)
ax[0].plot(t_ana, y_ana[1]*56, color='k')
ax[0].plot(t_ana, y_ana[2]*56, color='k')


# Plot the testrun
path_gear = 'test/ni56-decay_x-tfc/testrun/tracked_nuclei.dat'
time,fe56_xtfc,co56_xtfc,ni56_xtfc = np.loadtxt(path_gear,unpack=True)
time,fe56_xtfc,co56_xtfc,ni56_xtfc = time[:-1],fe56_xtfc[:-1],co56_xtfc[:-1],ni56_xtfc[:-1]
ax[0].plot(time, fe56_xtfc*56, color='tab:orange', linestyle='dashdot')
ax[0].plot(time, co56_xtfc*56, color='tab:green', linestyle='dashdot')
ax[0].plot(time, ni56_xtfc*56, color='tab:blue', linestyle='dashdot')

path_gear = 'test/ni56-decay_euler/testrun/tracked_nuclei.dat'
time_euler,fe56_euler,co56_euler,ni56_euler = np.loadtxt(path_gear,unpack=True)
time_euler,fe56_euler,co56_euler,ni56_euler = time_euler[:-1],fe56_euler[:-1],co56_euler[:-1],ni56_euler[:-1]
ax[0].plot(time_euler, fe56_euler*56, color='tab:orange', linestyle='dotted')
ax[0].plot(time_euler, co56_euler*56, color='tab:green', linestyle='dotted')
ax[0].plot(time_euler, ni56_euler*56, color='tab:blue', linestyle='dotted')

path_gear = 'test/ni56-decay_gear/testrun/tracked_nuclei.dat'
time_gear,fe56_gear,co56_gear,ni56_gear = np.loadtxt(path_gear,unpack=True)
time_gear,fe56_gear,co56_gear,ni56_gear = time_gear[:-1],fe56_gear[:-1],co56_gear[:-1],ni56_gear[:-1]
time_gear = np.delete(time_gear, 1)
fe56_gear = np.delete(fe56_gear, 1)
co56_gear = np.delete(co56_gear, 1)
ni56_gear = np.delete(ni56_gear, 1)
ax[0].plot(time_gear, fe56_gear*56, color='tab:orange', linestyle='dashed')
ax[0].plot(time_gear, co56_gear*56, color='tab:green', linestyle='dashed')
ax[0].plot(time_gear, ni56_gear*56, color='tab:blue', linestyle='dashed')


for i in range(subplots[0]):
    ax[i].vlines(time, 0, 1, color='lightgrey', linewidth=1.2)
    ax[i].grid(axis='y')


# Plot the errors
error_xtfc = abs(np.array([ni56_xtfc, co56_xtfc, fe56_xtfc]) - y_ana)*56
y_ana_euler = analyticSol(y0, time_euler)
error_euler = abs(np.array([ni56_euler, co56_euler, fe56_euler]) - y_ana_euler)*56
y_ana_gear = analyticSol(y0, time_gear)
error_gear = abs(np.array([ni56_gear, co56_gear, fe56_gear]) - y_ana_gear)*56

print('X-TFC', '{:e}'.format(np.nanmean(error_xtfc)))
print('Backward Euler', '{:e}'.format(np.nanmean(error_euler)))
print('Gear', '{:e}'.format(np.nanmean(error_gear)))


# Give labels and limits to the plot
plt.xlabel('Time [s]')
ax[0].set_ylabel('Mass fraction')
ax[0].set_xlim(1e4,1e8)
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[1].set_yscale('log')
ax[1].set_ylabel('Absolute error')
ax[1].set_ylim([1e-11, 1e-1])
ax[0].set_ylim([1e-9, 1e0])

ax[1].plot(time, error_xtfc[0, :], color='tab:orange', linestyle='dashdot')
ax[1].plot(time_euler, error_euler[0, :], color='tab:orange', linestyle='dotted')
ax[1].plot(time_gear, error_gear[0, :], color='tab:orange', linestyle='dashed')
ax[1].plot(time, error_xtfc[1, :], color='tab:green', linestyle='dashdot')
ax[1].plot(time_euler, error_euler[1, :], color='tab:green', linestyle='dotted')
ax[1].plot(time_gear, error_gear[1, :], color='tab:green', linestyle='dashed')
ax[1].plot(time, error_xtfc[2, :], color='tab:blue', linestyle='dashdot')
ax[1].plot(time_euler, error_euler[2, :], color='tab:blue', linestyle='dotted')
ax[1].plot(time_gear, error_gear[2, :], color='tab:blue', linestyle='dashed')


# Create legend
a1, = plt.plot(np.nan, np.nan, color='tab:blue')
a2, = plt.plot(np.nan, np.nan, color='tab:green')
a3, = plt.plot(np.nan, np.nan, color='tab:orange')
l1, = plt.plot(np.nan, np.nan, color='k')
l2, = plt.plot(np.nan, np.nan, color='tab:blue', linestyle='dotted')
l3, = plt.plot(np.nan, np.nan, color='tab:blue', linestyle='dashed')
l4, = plt.plot(np.nan, np.nan, color='tab:blue', linestyle='dashdot')
ax[0].legend([a1, a2, a3, l1, l2, l3, l4], ['$^{56}$Ni', '$^{56}$Co', '$^{56}$Fe', 'Analytic', 'Backward Euler', 'Gear', 'X-TFC'])


plt.savefig('test/ni56_test_bench.pdf', bbox_inches='tight')
plt.show()

