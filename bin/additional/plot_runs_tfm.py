import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_plot_size, set_subplots_size, set_width, tex_fonts


plt.rcParams.update(tex_fonts)

df = pd.read_table('runs/.runs.txt', sep=',')
tolerance = df['N-R Tolerance'].unique()
neurons = df['n Neurons'].unique()
isotopes = df['n Isotopes'].unique()
algorithms = df['Algorithm'].unique()
sparse = ['Sparse']


subplots = (3, 1)
fig, ax = plt.subplots(subplots[0], subplots[1], sharex=True, sharey=True,
                       figsize=set_subplots_size(width='tfm', fraction=.9,
                       subplots=subplots))
for i, n in enumerate(isotopes):
    dff = df.query('(`N-R Tolerance` == 1e-5) & (`n Isotopes` == @n)')\
            .groupby(['Algorithm', 'n Neurons', 'Sparse Solver']).mean('Execution Time').reset_index()
    for a in ['Euler', 'Gear']:
        dfff = dff.query('`Algorithm` == @a')
        ax[i].plot(dfff['n Neurons'], dfff['Execution Time'], marker='.', label=a)
    for a in sparse:
        dfff = dff.query('(`Algorithm` == "X-TFC") & (`Sparse Solver` == @a)')
        ax[i].plot(dfff['n Neurons'], dfff['Execution Time'], marker='.', label='X-TFC')
    ax[i].set_title(f'{n} isotopes')
    ax[i].set_ylabel('Execution time [s]')
    ax[i].grid()

ax[0].legend()
ax[-1].set_xlabel('\# neurons $|$ points')
plt.savefig('runs/time_neurons.pdf', bbox_inches='tight')
plt.show()


neurons = [2, 3, 5, 7, 10]
fig, ax = plt.subplots(subplots[0], subplots[1], sharex=True, sharey=True,
                       figsize=set_subplots_size(width='tfm', fraction=.85,
                                                 subplots=subplots))
for i, ni in enumerate(isotopes):
    dff = df.query('(`Algorithm` == "X-TFC") & (`n Isotopes` == @ni) & (`Sparse Solver` == "Sparse")')\
            .groupby(['n Neurons', 'N-R Tolerance']).mean('Execution Time').reset_index()
    for nn in neurons:
        dfff = dff.query('`n Neurons` == @nn')
        ax[i].plot(dfff['N-R Tolerance'], dfff['Execution Time'], marker='.', label=nn)
    ax[i].set_ylabel('Execution Time [s]')
    ax[i].set_title(f'{ni} isotopes')
    ax[i].grid()

ax[-1].set_xlabel('N-R Tolerance')
ax[0].set_xscale('log')
ax[0].invert_xaxis()
ax[0].legend()
plt.subplots_adjust(wspace=0)
plt.savefig('runs/time_tol.pdf', bbox_inches='tight')
plt.show()


fig, ax = plt.subplots(1, 1, figsize=set_plot_size(set_width('tfm')))
for i, n in enumerate(isotopes):
    dff = df.query('(`Algorithm` == "X-TFC") & (`N-R Tolerance` == 1e-5) & (`n Isotopes` == @n)')\
            .groupby(['n Neurons', 'Sparse Solver']).count().reset_index()
    plt.plot(dff['n Neurons'], dff['Execution Time'], marker='.', label=n)

plt.ylabel('\% convergence')
plt.xlabel('\# neurons $|$ points')
plt.legend(title='\# isotopes')
plt.grid()
plt.savefig('runs/con_neurons.pdf', bbox_inches='tight')
plt.show()

n_isotopes = ['6', '13', '18']
n_neurons = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
print('% of times X-TFC computes the solution until the final time with 1e-5 N-R tolerance')
print(len(df.query('(`Algorithm` == "X-TFC") & (`N-R Tolerance` == 1e-5) & ((`n Neurons` == 2) | (`n Neurons` == 3))'))/(len(n_isotopes)*2*100)*100)

