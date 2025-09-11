import sys
import pandas as pd
import matplotlib.pyplot as plt


file_path = sys.argv[1]
df = pd.read_csv(file_path)


marker_list = ['o-','o-','o-','o-']  
for (method, marker) in zip(df['Method'].unique(), marker_list):
    method_data = df[df['Method'] == method]
    plt.plot(method_data['BlockSize'], method_data['Total'], marker, label=method)

# Adding labels and title as per the example image
plt.xlabel('Block Size')
plt.ylabel('Time (sec)')
plt.xticks(df['BlockSize'].unique())
plt.xscale
plt.title('Kmeans {256,16,16,10}: Total Time vs. Block Size')
plt.legend()


plt.grid(True)

# Save the plot as a PNG file
plt.savefig('kmeans_all_coord16.png', dpi=300)

# Also display the plot
#plt.show()
