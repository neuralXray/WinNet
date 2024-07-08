from os import listdir
from os.path import exists
from re import search

#   2       3      4      5      6       7      8        9       10
# 1.1 1.04779 1.0312 1.0231 1.0183 1.01514 1.0129 1.011231 1.009911


n_isotopes = ['6', '13', '18']
nr_tol = ['1e-5', '1e-6', '1e-8', '1e-10', '1e-12']
n_neurons = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
timestep_max=['1.1', '1.04779', '1.0312', '1.0231', '1.0183', '1.01514', '1.0129', '1.011231', '1.009911']
use_sparse_solver = ['yes']
n_executions = 10


def read_last_line(file_name):
    with open(file_name, 'rb') as file:
        file.seek(-2, 2)
        while file.read(1) != b'\n':
            file.seek(-2, 1)
        return file.read().decode().strip()


runs_dir = 'runs/'
execution_regex = '^Example_He_burning_((' + ')|('.join(n_isotopes) + '))_x-tfc_((' + \
                  ')|('.join(nr_tol) + '))_((' + ')|('.join(n_neurons) + \
                  '))_((' + ')|('.join(use_sparse_solver) + '))_[0-9]{1,' + str(len(str(n_executions))) + '}$'
runs_dirs = [run_dir for run_dir in listdir(runs_dir) if search(execution_regex, run_dir)]
file = open(runs_dir + 'runs.txt', 'w')
file.write('n Isotopes,Algorithm,Execution Time,N-R Tolerance,n Neurons,Sparse Solver\n')
for ss in use_sparse_solver:
    if ss == 'yes':
        ssw = 'Sparse'
    else:
        ssw = 'No Sparse'
    for nn in n_neurons:
        for tol in nr_tol:
            for n in n_isotopes:
                execution_regex = '^Example_He_burning_' + n + '_x-tfc_' + tol + '_' + nn + '_' + \
                                  ss + '_[0-9]{1,' + str(len(str(n_executions))) + '}$'
                runs_dirs_n_a = [run_dir for run_dir in runs_dirs if search(execution_regex, run_dir)]
                for run_dir in runs_dirs_n_a:
                    out_dir = runs_dir + run_dir + '/OUT'
                    if exists(out_dir):
                        last_line = read_last_line(out_dir)
                        if last_line.startswith('Elapsed time [s]:'):
                            exec_time = last_line[last_line.rindex(' ') + 1:]
                            file.write(n + ',X-TFC,' + exec_time + ',' + tol + ',' + nn + ',' + ssw + '\n')


execution_regex = '^Example_He_burning_((' + ')|('.join(n_isotopes) + '))_gear_((' + \
                  ')|('.join(nr_tol) + '))_((' + ')|('.join(n_neurons) + \
                  '))_yes_[0-9]{1,' + str(len(str(n_executions))) + '}$'
runs_dirs = [run_dir for run_dir in listdir(runs_dir) if search(execution_regex, run_dir)]
for nn in n_neurons:
    for tol in nr_tol:
        for n in n_isotopes:
            execution_regex = '^Example_He_burning_' + n + '_gear_' + tol + '_' + nn + '_yes_[0-9]{1,' + \
                              str(len(str(n_executions))) + '}$'
            runs_dirs_n_a = [run_dir for run_dir in runs_dirs if search(execution_regex, run_dir)]
            for run_dir in runs_dirs_n_a:
                out_dir = runs_dir + run_dir + '/OUT'
                if exists(out_dir):
                    last_line = read_last_line(out_dir)
                    if last_line.startswith('Elapsed time [s]:'):
                        exec_time = last_line[last_line.rindex(' ') + 1:]
                        file.write(n + ',Gear,' + exec_time + ',' + tol + ',' + nn + ',Sparse\n')


execution_regex = '^Example_He_burning_((' + ')|('.join(n_isotopes) + '))_euler_((' + ')|('.join(nr_tol) + \
                  '))_((' + ')|('.join(timestep_max) + '))_yes_[0-9]{1,' + str(len(str(n_executions))) + '}$'
runs_dirs = [run_dir for run_dir in listdir(runs_dir) if search(execution_regex, run_dir)]
for tm, nn in zip(timestep_max, n_neurons):
    for tol in nr_tol:
        for n in n_isotopes:
            execution_regex = '^Example_He_burning_' + n + '_euler_' + tol + '_' + tm + '_yes_[0-9]{1,' + \
                              str(len(str(n_executions))) + '}$'
            runs_dirs_n_a = [run_dir for run_dir in runs_dirs if search(execution_regex, run_dir)]
            for run_dir in runs_dirs_n_a:
                out_dir = runs_dir + run_dir + '/OUT'
                if exists(out_dir):
                    last_line = read_last_line(out_dir)
                    if last_line.startswith('Elapsed time [s]:'):
                        exec_time = last_line[last_line.rindex(' ') + 1:]
                        file.write(n + ',Euler,' + exec_time + ',' + tol + ',' + nn + ',Sparse\n')

file.close()

