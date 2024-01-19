
import re
import matplotlib.pyplot as plt
import os
import sys

def extract_times(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    times = {2048: [], 4096: [], 6144: []}

    for line in lines:
        words = line.split()
        grid_size = int(words[2])
        computation_time = float(words[words.index('ComputationTime') + 1])
        total_time = float(words[words.index('TotalTime') + 1])

        if grid_size in times:
            times[grid_size].append((computation_time, total_time))

    return times

def plot_data(times, grid):
    print(times)

    proc = [8, 16, 32, 64]

    exec_times = times[grid]
    computation_times = [x[0] for x in exec_times]
    computation_times = [computation_times[0]/x for x in computation_times]

    total_times = [x[1] for x in exec_times]
    total_times = [total_times[0]/x for x in total_times]

    computation_times = computation_times[3:len(computation_times)]
    total_times = total_times[3:len(total_times)]
    bar_width = 0.35
    # Using indices for equally spaced x-axis values
    indices = range(len(proc))

    # Plot the computation times as bars
    plt.figure(figsize=(10, 6))
    plt.bar(indices, computation_times, bar_width, color='maroon', label='Computation Speedup')

    # Plot the total times as bars next to the computation times
    plt.bar([x + bar_width for x in indices], total_times, bar_width, color='blue', label='Total Speedup')

    plt.title(f"Jacobi_{grid}_speedup_plot")
    plt.xlabel("Processes")
    plt.ylabel("Speedup")
    plt.xticks([x + bar_width / 2 for x in indices], proc)  # Set x-axis ticks labels to processes
    plt.legend()  # Show legend for the two bars
    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

    plt.savefig(f"Jacobi_{grid}_speedup_plot", dpi=300)
    plt.close()

filename = sys.argv[1]
grid = int(sys.argv[2])
times = extract_times(filename)
plot_data(times,grid)