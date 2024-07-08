#!/bin/bash

#   2       3      4      5      6       7      8        9       10
# 1.1 1.04779 1.0312 1.0231 1.0183 1.01514 1.0129 1.011231 1.009911

n_isotopes=(6 13 18)
nr_tol=(1e-5)
n_neurons=(2 3 4 5 6 7 8 9 10)
timestep_max=(1.1 1.04779 1.0312 1.0231 1.0183 1.01514 1.0129 1.011231 1.009911)
sparse_solver=(yes)  # no)
MAX_EXEC_TIME=5


source winnet/bin/activate


#<<'###BLOCK-COMMENT'
for tol in "${nr_tol[@]}"; do
    paste <(printf "%s\n" "${n_neurons[@]}") <(printf "%s\n" "${timestep_max[@]}") | while IFS=$'\t' read -r nn tm; do
        python bin/additional/hiper_param_var.py $tol $nn $tm yes
        for n in "${n_isotopes[@]}"; do
            make clean
            make
            for i in {1..10}; do
                nice -n 1 python makerun.py -p "Example_He_burning_${n}_euler.par" -r "Example_He_burning_${n}_euler_${tol}_${tm}_yes_${i}" --force > /dev/null 2>&1 &
                PID=$!
                sleep $MAX_EXEC_TIME
                if ps -p $PID > /dev/null; then
                    pkill -9 -f "Example_He_burning"
                    sleep $MAX_EXEC_TIME
                fi
            done
        done
    done
done
###BLOCK-COMMENT

#<<'###BLOCK-COMMENT'
for tol in "${nr_tol[@]}"; do
    for nn in "${n_neurons[@]}"; do
        python bin/additional/hiper_param_var.py $tol $nn 1.1 yes
        for n in "${n_isotopes[@]}"; do
            make clean
            make
            for i in {1..10}; do
                nice -n 1 python makerun.py -p "Example_He_burning_${n}_gear.par" -r "Example_He_burning_${n}_gear_${tol}_${nn}_yes_${i}" --force > /dev/null 2>&1 &
                PID=$!
                sleep $MAX_EXEC_TIME
                if ps -p $PID > /dev/null; then
                    pkill -9 -f "Example_He_burning"
                    sleep $MAX_EXEC_TIME
                fi
            done
        done
    done
done
###BLOCK-COMMENT


#<<'###BLOCK-COMMENT'
for ss in "${sparse_solver[@]}"; do
    for tol in "${nr_tol[@]}"; do
        for nn in "${n_neurons[@]}"; do
            python bin/additional/hiper_param_var.py $tol $nn 1.1 $ss
            for n in "${n_isotopes[@]}"; do
                make clean
                make
                for i in {1..10}; do
                    nice -n 1 python makerun.py -p "Example_He_burning_${n}_x-tfc.par" -r "Example_He_burning_${n}_x-tfc_${tol}_${nn}_${ss}_${i}" --force > /dev/null 2>&1 &
                    PID=$!
                    sleep $MAX_EXEC_TIME
                    if ps -p $PID > /dev/null; then
                        pkill -9 -f "Example_He_burning"
                        sleep $MAX_EXEC_TIME
                    fi
                done
            done
        done
    done
done
###BLOCK-COMMENT



n_isotopes=(6 13 18)
nr_tol=(1e-6 1e-8 1e-10 1e-12)
n_neurons=(2 3 5 7 10)
timestep_max=(1.1 1.04779 1.0231 1.01514 1.009911)
sparse_solver=(yes)  # no)
MAX_EXEC_TIME=5


source winnet/bin/activate


#<<'###BLOCK-COMMENT'
for tol in "${nr_tol[@]}"; do
    paste <(printf "%s\n" "${n_neurons[@]}") <(printf "%s\n" "${timestep_max[@]}") | while IFS=$'\t' read -r nn tm; do
        python bin/additional/hiper_param_var.py $tol $nn $tm yes
        for n in "${n_isotopes[@]}"; do
            make clean
            make
            for i in {1..10}; do
                nice -n 1 python makerun.py -p "Example_He_burning_${n}_euler.par" -r "Example_He_burning_${n}_euler_${tol}_${tm}_yes_${i}" --force > /dev/null 2>&1 &
                PID=$!
                sleep $MAX_EXEC_TIME
                if ps -p $PID > /dev/null; then
                    pkill -9 -f "Example_He_burning"
                    sleep $MAX_EXEC_TIME
                fi
            done
        done
    done
done
###BLOCK-COMMENT

#<<'###BLOCK-COMMENT'
for tol in "${nr_tol[@]}"; do
    for nn in "${n_neurons[@]}"; do
        python bin/additional/hiper_param_var.py $tol $nn 1.1 yes
        for n in "${n_isotopes[@]}"; do
            make clean
            make
            for i in {1..10}; do
                nice -n 1 python makerun.py -p "Example_He_burning_${n}_gear.par" -r "Example_He_burning_${n}_gear_${tol}_${nn}_yes_${i}" --force > /dev/null 2>&1 &
                PID=$!
                sleep $MAX_EXEC_TIME
                if ps -p $PID > /dev/null; then
                    pkill -9 -f "Example_He_burning"
                    sleep $MAX_EXEC_TIME
                fi
            done
        done
    done
done
###BLOCK-COMMENT


#<<'###BLOCK-COMMENT'
for ss in "${sparse_solver[@]}"; do
    for tol in "${nr_tol[@]}"; do
        for nn in "${n_neurons[@]}"; do
            python bin/additional/hiper_param_var.py $tol $nn 1.1 $ss
            for n in "${n_isotopes[@]}"; do
                make clean
                make
                for i in {1..10}; do
                    nice -n 1 python makerun.py -p "Example_He_burning_${n}_x-tfc.par" -r "Example_He_burning_${n}_x-tfc_${tol}_${nn}_${ss}_${i}" --force > /dev/null 2>&1 &
                    PID=$!
                    sleep $MAX_EXEC_TIME
                    if ps -p $PID > /dev/null; then
                        pkill -9 -f "Example_He_burning"
                        sleep $MAX_EXEC_TIME
                    fi
                done
            done
        done
    done
done
###BLOCK-COMMENT

