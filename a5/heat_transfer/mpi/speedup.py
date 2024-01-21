import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def extract_times(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    times = {}

    for line in lines:
        words = line.split()
        method = words[0]
        grid_size = int(words[2])  
        computation_time = float(words[words.index('ComputationTime') + 1])
        total_time = float(words[words.index('TotalTime') + 1])
        mpi_process = str(int(words[words.index('Px') + 1])*int(words[words.index('Py') + 1]))  # Convert mpi_process to string

        if grid_size not in times:
            times[grid_size] = {}
        if mpi_process not in times[grid_size]:
            times[grid_size][mpi_process] = {}
        if method not in times[grid_size][mpi_process]:
            times[grid_size][mpi_process][method] = []

        times[grid_size][mpi_process][method].append((computation_time, total_time))

    return times

def calculate_speedup(times):
    speedup = {}

    for grid_size, mpi_processes in times.items():
        speedup[grid_size] = {}
        for mpi_process, methods in mpi_processes.items():
            speedup[grid_size][mpi_process] = {}
            for method, exec_times in methods.items():
                base_time = times[grid_size]["1"][method][0][0]  # Assuming computation time is the first element in the tuple
                current_time = exec_times[0][0]  # Assuming computation time is the first element in the tuple
                speedup[grid_size][mpi_process][method] = base_time / current_time

    return speedup


def plot_speedup(speedup):
    bar_width = 0.2
    # Get the list of methods
    methods = list(next(iter(next(iter(speedup.values())).values())).keys())
    # Get the list of mpi_processes
    mpi_processes = list(map(int, next(iter(speedup.values())).keys()))
    mpi_processes.sort()

    n_methods = len(methods)
    n_processes = len(mpi_processes)

    for grid_size in speedup.keys():
        plt.figure(figsize=(10, 6))

        for i, method in enumerate(methods):
            speedup_values = [speedup[grid_size][str(mpi_process)][method] for mpi_process in mpi_processes]
            bar_positions = np.arange(n_processes) + i * bar_width
            plt.bar(bar_positions, speedup_values, bar_width, label=method)

        plt.title(f"Speedup_plot_{grid_size}")
        plt.xlabel("Number of Processes")
        plt.ylabel("Speedup")
        plt.xticks(np.arange(n_processes) + bar_width * (n_methods - 1) / 2, mpi_processes)  # Set x-axis ticks labels to mpi_processes
        plt.legend()  # Show legend for the two bars
        plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

        plt.savefig(f"Speedup_plot_{grid_size}", dpi=300)
        plt.close()
filename = sys.argv[1]
times = extract_times(filename)
speedup = calculate_speedup(times)
plot_speedup(speedup)