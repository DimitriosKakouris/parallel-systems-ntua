import matplotlib.pyplot as plt
import numpy as np
import sys

# Read data from file
file1 = open(sys.argv[1], 'r')
lines = file1.readlines()
file1.close()

times = [float(line.strip('\n')) for line in lines]

# Organizing data into groups
groups = [times[i:i+8] for i in range(0, len(times), 8)]
print(groups)
# Thread configurations
threads = [1, 2, 4, 8, 16, 32, 64, 128]

# Number of groups and threads
num_groups = len(groups)
num_threads = len(threads)

# Setting up the figure and axes
fig, ax = plt.subplots(figsize=(15, 8))

# Width of a bar
bar_width = 0.1

# Base x-coordinates for each thread configuration
base_indices = np.arange(num_threads)
# secondary_indices = np.arange(4)
# Colors for different bars in a group
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']


configs=["100-0-0","80-10-10","20-40-40","0-50-50"]
# Looping over each group and plotting the bars
for i, group in enumerate(groups):
    # Adjust x-coordinates for each bar
    indices = base_indices + i * bar_width
    print(indices)
    print(group)

    # for _ in range(4): group.append(0)
    # Plotting the bars for each thread configuration
    ax.bar(indices, group, bar_width, label=f'{configs[i%num_threads]}', color=colors[i % len(colors)])

# Setting the x-axis ticks and labels
ax.set_xticks(base_indices + bar_width * (num_groups - 1) / 2)
ax.set_xticklabels(threads)

# Adding labels and title
ax.set_xlabel('Thread Configurations')
ax.set_ylabel('Kops/sec')
ax.set_title('Optimistic Sync 1024 across Different Thread Configurations')

# Adding a legend
ax.legend()
plt.savefig('Optimistic Sync 1024.png')
plt.plot(dpi=300)



