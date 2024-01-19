#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans

## Output and error files
#PBS -o gpu.out
#PBS -e gpu.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=40

##How long should the job run for?
#PBS -l walltime=00:30:00

## Start 
## Run make in the src folder (modify properly)

cd /home/parallel/parlab09/ex4_dimitris/kmeans

make get_gpu_info

./get_gpu_info
#nvidia-smi