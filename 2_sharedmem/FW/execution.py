import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV data
file_path = 'execution_times.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Separate data by array size
sizes = [1024, 2048, 4096]
data_by_size = {size: data[data['Size'] == size] for size in sizes}

# Function to plot data for a specific size

def plot_data_for_size(size, data, ax):
    # Get unique number of cores
    cores = sorted(data['NumberOfCores'].unique())
    bar_width = 0.35

    # Plotting for each block size
    for block_size in [64, 128]:
        times = data[data['BlockSize'] == block_size]['Time']
        offset = -bar_width/2 if block_size == 64 else bar_width/2
        ax.bar([x + offset for x in range(len(cores))], times, bar_width, label=f'BlockSize {block_size}')

    ax.set_xlabel('Number of Threads')
    ax.set_ylabel('Execution Time')
    ax.set_title(f'Execution Time for Array Size {size}')
    ax.set_xticks(range(len(cores)))
    ax.set_xticklabels(cores)
    ax.legend()


# Create plots
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

for i, size in enumerate(sizes):
    plot_data_for_size(size, data_by_size[size], axes[i])

plt.tight_layout()
plt.savefig("execution_times_sr.png")
