#!/bin/bash

# Load the openmp module
module load openmp
cd /home/parallel/parlab09/ex2_dimitris/FW
# N and B are passed as environment variables
for threads in 1 2 4 8 16 32 64; do
    export OMP_NUM_THREADS=$threads
    ./fw_sr_par2 $N $B
done

