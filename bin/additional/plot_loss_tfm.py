import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/home/jax/Documents/TFM/latex/')
from my_plot import set_subplots_size, tex_fonts


plt.rcParams.update(tex_fonts)
fig, ax = plt.subplots(1, 1, figsize=set_plot_size(set_width('tfm')))


n = 18
directory = f'runs/.Example_He_burning_{n}_loss/'
df = pd.read_table(directory + 'loss.txt', sep=' +', engine='python')
df.columns = ['time', 'it', 'loss']
print(df['it'].max())

plt.figure()
for time in df['time'].quantile([0, .25, .5, .75, 1]):
    dff = df.query('`time` == @time')
    plt.plot(dff['it'], dff['loss'] / dff.query('`it` == 0')['loss'].values, marker='.', label='{:.1e}'.format(time))

plt.yscale('log')
plt.grid()
plt.legend(title='Time [s]')
plt.xlabel('\# N-R iterations')
plt.ylabel('L/L$^0$')
plt.savefig(directory + 'loss.pdf', bbox_inches='tight')
plt.show()



n = 18
for nn in [2, 3, 4, 5]:
    df = pd.read_table(f'runs/.Example_He_burning_{n}_{nn}_loss/loss.txt', sep=' +', engine='python')
    df.columns = ['time', 'it', 'loss']
    print(df['it'].max())
    dff = df.query('`it` == 10').set_index('time')
    dff0 = df.query('`it` == 0').set_index('time')
    dff['loss'] = dff['loss'] / dff0['loss']
    plt.plot(dff.index, dff['loss'], label=nn)

plt.yscale('log')
plt.xscale('log')
plt.ylim([1e-18, 1e-4])
plt.grid()
plt.legend(title='$n_n | n_x$')
plt.ylabel('$L^{10} / L^0$')
plt.xlabel('Time [s]')
plt.savefig('runs/loss_10.pdf', bbox_inches='tight')
plt.show()

