#!/bin/bash

cd /home/parallel/parlab09/ex2_dimitris/FW

for N in 1024 2048 4096; do
    for B in 64 128; do
        qsub -N run_omp_game_N_${N}_B_${B} \
             -o run_fw_N_${N}_B_${B}.out \
             -e run_fw_N_${N}_B_${B}.err \
             -v N=${N},B=${B} \
             -l nodes=sandman:ppn=64 \
	     -q serial \
             -l walltime=00:20:00 \
             job_script.sh
    done
done
