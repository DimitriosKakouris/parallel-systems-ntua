import re
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np

# Function to parse the data and write to CSV
def parse_data_to_csv(file_name,csv_file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    pattern = r'(\w+) X (\d+) Y (\d+) Px (\d+) Py (\d+) Iter (\d+) ComputationTime ([\d.]+) TotalTime ([\d.]+)'
    matches = re.finditer(pattern, data)

    with open(csv_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Method', 'GridSizeX', 'GridSizeY', 'Px', 'Py', 'Iterations', 'ComputationTime', 'TotalTime'])

        for match in matches:
            writer.writerow([
                match.group(1),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
                int(match.group(5)),
                int(match.group(6)),
                float(match.group(7)),
                float(match.group(8))
            ])

# Function to read the CSV file and return data organized by MPI process configuration
def read_csv_data(csv_file_name):
    data = {}
    with open(csv_file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mpi_processes = int(row['Px']) * int(row['Py'])
            key = (mpi_processes, row['Method'])
            if key not in data:
                data[key] = []
            data[key].append(float(row['TotalTime']))
    return data

# Function to plot the grouped bar plot
def plot_speedup_graph(data):
    # Unique sorted list of MPI process counts
    mpi_processes = sorted(list(set(key[0] for key in data.keys())))

    grid_sizes = [2048,4096,6144]  
    print(grid_sizes)
    # Methods in the order they should be displayed
    methods = ['Jacobi', 'GaussSeidelSOR', 'RedBlackSOR']

    bar_width = 0.2
    opacity = 0.8

    

    for k,grid_size in enumerate(grid_sizes):
        fig,ax = plt.subplots()
        times=[]
        baseline_time = None
        for j in mpi_processes:
          
            method_times = [data[(j, method)][k] for method in methods]
            if j == 1:
                baseline_time = method_times
            times.append([baseline_time[i] / time if time != 0 else 0 for i, time in enumerate(method_times)])
           
           

        # Create the bar plot
        for i in range(len(methods)):
            ax.bar(np.arange(len(mpi_processes)) + i*bar_width, [time[i] for time in times], bar_width, alpha=opacity, label=methods[i])

        ax.set_xlabel('MPI Processes')
        ax.set_ylabel('Seq/time (seconds)')
        ax.set_title(f'Speedup for Grid Size {grid_size}x{grid_size}')
        ax.set_xticks(np.arange(len(mpi_processes)) + bar_width, mpi_processes)
        ax.legend()
        plt.savefig(f'Speedup for Grid Size {grid_size}x{grid_size}', dpi=300)

      
   
    
# Usage
file_name = sys.argv[1]  # Use your file name
parse_data_to_csv(file_name, 'all_noconv.csv')
csv_file_name = 'all_noconv.csv'
data = read_csv_data(csv_file_name)

plot_speedup_graph(data)
