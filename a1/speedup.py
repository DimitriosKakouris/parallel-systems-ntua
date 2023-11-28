import matplotlib.pyplot as plt
import numpy as np
import sys

file1 = open(sys.argv[1], 'r')
lines = file1.readlines()

times=[]
threads=[1,2,4,6,8]

file1.close()

for line in lines:
    times.append(float(line.split(' ')[6]))

print(times)

n=np.linspace(1,9,200)
inv_n=n


speedup=times[0]/np.array(times)

plt.figure(dpi=300)
plt.xlabel('Threads')
plt.ylabel('Speedup')
grid=int(sys.argv[1].split('_')[3].split('.')[0])

plt.title("Speedup vs. Number of threads "+repr(grid)) 
plt.plot(threads,speedup, marker='o',label='real')
plt.plot(n,inv_n,color='green', linestyle='dashed',label="theoretical")
plt.xticks([1,2,4,6,8]);
plt.legend(loc="upper right")
plt.savefig('speedup_'+ repr(grid) +'.png')

