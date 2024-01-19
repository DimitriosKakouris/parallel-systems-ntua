import csv
import matplotlib.pyplot as plt
import os

import sys


def extract_data(filename):
    data = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            type = row[0]
            block_size = int(row[1])
            exec_time = float(row[-1])
            if type not in data:
                data[type] = []
            data[type].append((block_size, exec_time*1000))
      
    return data


def plot_data(data, directory='.'):
    sequential_time = 9.710023*1000
    
    for type, values in data.items():
      
        values.sort(key=lambda x: x[0])  # Sort by block size
        block_sizes = [x[0] for x in values]
        exec_times = [x[1] for x in values]
        exec_times = [sequential_time/x for x in exec_times]

        # Using indices for equally spaced x-axis values
        indices = range(len(block_sizes))
        
        plt.figure(figsize=(10, 6))
        plt.plot(indices, exec_times, color='maroon', marker='o')
        plt.title(f"{type.replace('-', '')} - Speedup vs Block Size")
        plt.xlabel("Block Size")
        plt.ylabel("Speedup")
        plt.xticks(indices, block_sizes)  # Set x-axis ticks labels to block sizes
        plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

        plot_path = os.path.join(directory, f"{type.replace('-', '')}_speedup_plot.png")
        plt.savefig(plot_path,dpi=300)
    
        plt.close()

filename = sys.argv[1]
data = extract_data(filename)
plot_data(data)
