from sys import argv


nr_tol = argv[1]
nneurons_nx = argv[2]
timestep_max = argv[3]
sparse_solver = argv[4]

n_isotopes = ['6', '13', '18']
algorithms = ['x-tfc', 'euler', 'gear']

par_dir = 'par/'
for a in algorithms:
    for n in n_isotopes:
        file = open(f'{par_dir}Example_He_burning_{n}_{a}.par', 'r')
        par_data = file.readlines()
        file.close()
        file = open(f'{par_dir}Example_He_burning_{n}_{a}.par', 'w')
        for line in par_data:
            if line.startswith('nr_tol = '):
                file.write(f'nr_tol = {nr_tol}\n')
            elif line.startswith('gear_nr_eps = '):
                file.write(f'gear_nr_eps = {nr_tol}\n')
            elif line.startswith('n_neurons = '):
                file.write(f'n_neurons = {nneurons_nx}\n')
            elif line.startswith('n_x = '):
                file.write(f'n_x = {nneurons_nx}\n')
            elif (a != 'x-tfc') & line.startswith('timestep_max = '):
                file.write(f'timestep_max = {timestep_max}\n')
            elif line.startswith('trajectory_file = '):
                file.write(f'trajectory_file = @WINNET@/data/Example_data/Example_He_burning_{n}_gear/trajectory_{nneurons_nx}\n')
            elif (a != 'x-tfc') & line.startswith('out_every = '):
                value = 10 * (int(nneurons_nx) - 1)
                file.write(f'out_every = {value}\n')
            elif (a != 'x-tfc') & line.startswith('mainout_every = '):
                value = int(nneurons_nx) - 1
                file.write(f'mainout_every = {value}\n')
            elif (a != 'x-tfc') & line.startswith('engen_every = '):
                value = int(nneurons_nx) - 1
                file.write(f'engen_every = {value}\n')
            elif (a != 'x-tfc') & line.startswith('track_nuclei_every = '):
                value = int(nneurons_nx) - 1
                file.write(f'track_nuclei_every = {value}\n')
            elif (a == 'x-tfc') & line.startswith('use_sparse_solver = '):
                file.write(f'use_sparse_solver = {sparse_solver}\n')
            else:
                file.write(line)
        file.close()

