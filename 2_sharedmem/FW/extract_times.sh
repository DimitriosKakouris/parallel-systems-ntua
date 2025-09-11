#!/bin/bash

output_file="execution_times.csv"

# Write the header to the output file
echo "File,Size,BlockSize,NumberOfCores,Time" > "$output_file"

# Define an array for the number of cores
cores=(1 2 4 8 16 32 64)

# Loop over each file matching the pattern run_fw_N_*_B_*.out
for file in run_fw_N_*_B_*.out
do
    # Extract the size (N) and the block size (B) from the filename
    size=$(echo $file | sed -n 's/.*_N_\([0-9]\+\)_B_.*\.out/\1/p')
    blockSize=$(echo $file | sed -n 's/.*_B_\([0-9]\+\)\.out/\1/p')
    
    # Loop through the file and extract times for each core count
    for i in "${!cores[@]}"; do
        coreCount=${cores[$i]}
        time=$(awk "NR==$(($i+1))" "$file" | awk -F ',' '{print $4}')
        echo "$file,$size,$blockSize,$coreCount,$time" >> "$output_file"
    done
done

echo "Data saved to $output_file"

