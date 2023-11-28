#!/bin/bash
## Give the Job a descriptive name nvidia-s
#PBS -N run_kmeans
## Output and error files
#PBS -o nvidia.out 
#PBS -e nvidia.err
## How many machines should we get?
#PBS -l nodes=1:ppn=8
##How long should the job run for?
#PBS -l walltime=00:10:00
## Start Run make in the src folder (modify properly)

cd /home/parallel/parlab09/ex2_dimitris/kmeans
export CUDA_VISIBLE_DEVICES=1
dmidecode   
