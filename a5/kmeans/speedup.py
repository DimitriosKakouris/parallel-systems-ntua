import matplotlib.pyplot as plt
import os
import re
import sys


def extract_data(filename):
    data = []
    with open(filename, 'r') as file:
        for row in file:
            match = re.search(r'total\s*=\s*(\d+\.\d+)', row)
            if match:
                data.append(float(match.group(1)))
    return data


def plot_data(data, directory='.'):
    print(data)
    sequential_time = data[0]
    
    proc = [1,2,4,8,16,32,64]
    exec_times = data
    exec_times = [sequential_time/x for x in exec_times]

    # Using indices for equally spaced x-axis values
    # indices = range(len(proc))
    
    plt.figure(figsize=(10, 6))
    plt.plot(proc, exec_times, color='maroon', marker='o')
    plt.title("Kmeans MPI Speedup vs Processes")
    plt.xlabel("Processes")
    plt.ylabel("Speedup")
    # plt.xticks(indices,proc)  # Set x-axis ticks labels to block sizes
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

    
    plt.savefig("kmeans_mpi_speedup_plot",dpi=300)

    plt.close()

filename = sys.argv[1]
data = extract_data(filename)
plot_data(data)
