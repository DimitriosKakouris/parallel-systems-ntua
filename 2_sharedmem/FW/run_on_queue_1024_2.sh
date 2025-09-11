#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_omp_game

## Output and error files
#PBS -o run_fw_4096_2.out
#PBS -e run_fw_2048.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=64

##How long should the job run for?
#PBS -l walltime=01:00:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab09/ex2_thomas/FW

for threads in 1 2 4 6 8 16 32 64
do

export OMP_NUM_THREADS=${threads}
./fw_sr_par2 4096 64

done

