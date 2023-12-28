import re
import matplotlib.pyplot as plt
import os
import sys

def extract_data(filename):
    data = {}
    current_block_size = None
    current_type = None

    with open(filename, 'r') as file:
 
        for line in file:
            # Check for block size
            block_size_match = re.search(r'block_size = (\d+)', line)
            if block_size_match:
                current_block_size = int(block_size_match.group(1))
                continue

            # Check for section header
            header_match = re.search(r'\|\-(.+?)\-\|', line)
            if header_match:
                current_type = header_match.group(1).strip()
                continue

            # Check for total time
            if current_type and current_block_size is not None:
                total_time_match = re.search(r'total = ([\d.]+) ms', line)
                if total_time_match:
                    total_time = float(total_time_match.group(1))
                    if current_type not in data:
                        data[current_type] = []
                    data[current_type].append((current_block_size, total_time))

    with open(filename, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            
            if "|-------------Sequential Kmeans-------------|" in line:
                total_line = lines[i+4]
                total_seq = total_line.split('=')[2].strip().split(' ')[0]
                break
        for key in data:
            data[key].insert(0,(-1, float(total_seq)))
                
    print(data)
    return data

def plot_data(data, directory='.'):
    
    for type, values in data.items():
        values.sort(key=lambda x: x[0])  # Sort by block size
        block_sizes = [x[0] for x in values]
        exec_times = [x[1] for x in values]

        # Using indices for equally spaced x-axis values
        indices = range(len(block_sizes))
        
        plt.figure(figsize=(10, 6))
        plt.bar(indices, exec_times, color='maroon')
        plt.title(f"{type.replace('-', '')} - Execution Time vs Block Size")
        plt.xlabel("Block Size")
        plt.ylabel("Execution Time (ms)")
        plt.xticks(indices, block_sizes)  # Set x-axis ticks labels to block sizes
        plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

        plot_path = os.path.join(directory, f"{type.replace('-', '')}_execution_plot.png")
        plt.savefig(plot_path,dpi=300)
    
        plt.close()

filename = sys.argv[1]
data = extract_data(filename)
plot_data(data)
