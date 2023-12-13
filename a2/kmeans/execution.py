import matplotlib.pyplot as plt
import numpy as np
import sys

file1 = open(sys.argv[1], 'r')
lines = file1.readlines()

times = []
threads = [1, 2, 4, 8, 16, 32, 64]
bar_widths = [0.5, 1, 2, 4, 8, 16, 32]  # Custom bar widths

file1.close()

for line in lines:
    times.append(float(line.strip('\n')))

print(times)

n = np.linspace(1, 65, 200)
inv_n = n

plt.figure(dpi=300)
plt.xlabel('Threads')
plt.ylabel('Time(Sec)')
plt.title("Time vs. Number of threads - Reduction countering False Sharing ")
# Use custom widths for bars
for i, thread in enumerate(threads):
    plt.bar(thread, times[i], width=bar_widths[i], align='center', label=f"Thread {thread}" if i == 0 else "",color='maroon')

# plt.plot(n, inv_n, color='green', linestyle='dashed', label="theoretical")
plt.xscale('log', base=2)  # Use logarithmic scale with base 2 for x-axis
plt.xticks(threads, labels=threads)


# plt.grid(True, which="both", ls="--", c='0.7')  # Adding a grid for better visualization
plt.savefig('Execution Time' + '.png')

