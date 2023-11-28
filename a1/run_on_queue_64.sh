#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_omp_game

## Output and error files
#PBS -o run_omp_game_64.out
#PBS -e run_omp_game_64.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=00:05:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab09/ex1_dimitris

for threads in 1 2 4 6 8
do
module load openmp
export OMP_NUM_THREADS=${threads}
./Game_Of_Life 64 1000

done

