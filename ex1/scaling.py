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
plt.xlabel('Threads')  
plt.ylabel('Time')  

n=np.linspace(1,9,200)
inv_n=times[0]/n
plt.figure(dpi=300)
plt.xlabel('Threads')
plt.ylabel('Time')
grid=int(sys.argv[1].split('_')[3].split('.')[0])

plt.title("Execution time vs. Number of threads "+repr(grid)) 
plt.plot(threads, times, marker='o',label='real')
plt.plot(n,inv_n,color='green', linestyle='dashed',label="theoretical")
plt.xticks([1,2,4,6,8]);
plt.legend(loc="upper right")
plt.savefig('scaling_'+ repr(grid) +'.png')

