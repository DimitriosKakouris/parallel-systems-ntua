import csv
import sys
import matplotlib.pyplot as plt
import os

import numpy as np

def process_csv(file_name):
    # Dictionary to hold the data
    data_dict = {}

    with open(file_name, mode='r') as file:
        reader = csv.reader(file)

        for row in reader:
            # Check if the first column's value is already a key in the dictionary
            key = row[0]
            if key not in data_dict:
                data_dict[key] = []

            # Add the last three columns of the current row to the dictionary
            data_dict[key].append(row[-4:])

    return data_dict

# Replace 'your_file.csv' with your actual CSV file's name
data = process_csv(sys.argv[1])
print(data)

def plot_data(data, directory='.'):
    block_sizes = [32,64,128,256,512,1024]
    indices = np.arange(len(block_sizes))  # the x locations for the groups

    for type, values in data.items():
        # Create a figure and a set of subplots for each type
        fig, ax = plt.subplots()

        exec_times = np.array([[float(x[i]) for i in range(4)] for x in values])

        # Create a stacked bar for each type and block size

        ax.bar(indices, exec_times[:, 0], label='GPU->CPU', color='maroon')
        ax.bar(indices, exec_times[:, 1], bottom=exec_times[:, 0], label='CPU->GPU', color='orange')
        ax.bar(indices, exec_times[:, 2], bottom=exec_times[:, 0] + exec_times[:, 1], label='GPU', color='darkgreen')
        ax.bar(indices, exec_times[:, 3], bottom=exec_times[:, 0] + exec_times[:, 1] + exec_times[:, 2], label='CPU', color='lightblue')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Block Size')
        ax.set_ylabel('Parts Time (ms)')
        ax.set_title(f'{type} - Parts vs Block Size')
        ax.set_xticks(indices)
        ax.set_xticklabels(block_sizes)
        
        ax.legend()

        # Save the figure
        plt.savefig(f'{directory}/{type}_alt_transfer_plot.png', dpi=300)
     
plot_data(data)