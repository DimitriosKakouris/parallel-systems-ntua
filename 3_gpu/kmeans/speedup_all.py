import sys
import pandas as pd
import matplotlib.pyplot as plt

file_path = sys.argv[1]
df = pd.read_csv(file_path)

# Calculate the baseline time for the smallest block size
baseline_time = 9.710023 # Sequential time used for all plots

methods = df['Method'].unique()
num_methods = len(methods)

fig, axs = plt.subplots(2, 2, figsize=(12, 8))

for i, method in enumerate(methods):
    row = i // 2
    col = i % 2
    method_data = df[df['Method'] == method]
    # Calculate the speedup
    speedup = baseline_time / method_data['Total']
    axs[row, col].plot(method_data['BlockSize'], speedup, 'o-', label=method)

    # Adding labels and title
    axs[row, col].set_xlabel('Block Size')
    axs[row, col].set_ylabel('Speedup')
    axs[row, col].set_xticks(df['BlockSize'].unique())
    axs[row, col].set_title(f'Kmeans {256,16,16,10}: Speedup vs. Block Size for {method}')
    axs[row, col].legend()
    axs[row, col].grid(True)

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('kmeans_all_coord16_speedup.png', dpi=300)

# Also display the plot
#plt.show()