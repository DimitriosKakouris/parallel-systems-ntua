#!/bin/bash

## Give the Job a descriptive name  
#PBS -N runjob

## Output and error files
#PBS -o gs_conv.out
#PBS -e gs_conv.err

## How many machines should we get?
#PBS -l nodes=8:ppn=8

#PBS -l walltime=00:30:00

## Start
## Run make in the src folder (modify properly)

module load openmpi/1.8.3

cd /home/parallel/parlab09/ex5_dimitris/heat_transfer/mpi



mpirun --mca btl tcp,self -np 64 --map-by node ./gs_conv 1024 1024 8 8

