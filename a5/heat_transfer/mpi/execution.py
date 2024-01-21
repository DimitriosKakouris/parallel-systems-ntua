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




# Function to read the CSV file and return data organized by grid size and MPI process configuration
def read_csv_data(csv_file_name):
    data = {}
    with open(csv_file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['GridSizeX'], row['GridSizeY'], row['Px'], row['Py'])
            if key not in data:
                data[key] = []
            data[key].append(row)
    return data

# Function to plot the data
def plot_data(data):
    for key in data.keys():
        methods = [row['Method'] for row in data[key]]
        computation_times = [float(row['ComputationTime']) for row in data[key]]
        total_times = [float(row['TotalTime']) for row in data[key]]

        # Creating bar plots
        plt.figure(figsize=(10, 6))
        x = np.arange(len(methods))


        bar_width = 0.4
        plt.bar(x - bar_width/2, computation_times, width=bar_width, label='Computation Time', align='center')
        plt.bar(x + bar_width/2, total_times, width=bar_width, label='Total Time', align='center')

        plt.xlabel('Method')
        plt.ylabel('Time (seconds)')
        plt.title(f'Execution Times for Grid Size {key[0]}x{key[1]} and MPI Processes {int(key[2])*int(key[3])}')
        plt.xticks(x, methods)
        plt.legend()
        plt.savefig(f'Execution_times_{key[0]}_{int(key[2])*int(key[3])}.png',dpi=300)

# Usage
file_name = sys.argv[1]  # Use your file name
parse_data_to_csv(file_name, 'all_noconv.csv')
csv_file_name = 'all_noconv.csv'
data = read_csv_data(csv_file_name)
plot_data(data)