#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans

## Output and error files
#PBS -o run_kmeans_reduction.out
#PBS -e run_kmeans_reduction.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=64

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

cd /home/parallel/parlab09/ex3_dimitris/conc_ll
# Flatten the array
arr=(1024 100 0 0 1024 80 10 10 1024 20 40 40 1024 0 50 50 8092 100 0 0 8092 80 10 10 8092 20 40 40 8092 0 50 50)
MT_CONF=0,1,2,3
# Iterate over the array in steps
for ((i=0; i<${#arr[@]}; i+=4))
do
    ./x.serial ${arr[i]} ${arr[i+1]} ${arr[i+2]} ${arr[i+3]}
done
