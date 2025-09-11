import matplotlib.pyplot as plt
import sys
import re

def read_execution_times(filename):
    with open(filename, 'r') as file:
        times = [float(line.strip()) for line in file]
    return times

def calculate_speedup(times):
    base_time = times[0]  # Assuming the first line is the time for 1 thread
    return [base_time / time for time in times]

def plot_speedup(speedups, thread_counts,type_of_implementation):
    plt.figure(dpi=300)
    x_ticks = range(len(thread_counts))  # Equidistant ticks for the x-axis
    plt.plot(x_ticks, speedups, marker='o', color='maroon')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup')
    plt.title("Speedup vs. Number of threads - " + type_of_implementation)
    plt.xticks(x_ticks, thread_counts)  # Set the labels to be the thread counts
    plt.savefig('Speedup- '+ type_of_implementation + '.png')

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    # Extracting the type of implementation from the filename
    filename = sys.argv[1]
    type_of_implementation = re.search(r"times_(.*?)\.txt", filename).group(1)

    times = read_execution_times(filename)
    thread_counts = [1, 2, 4, 8, 16, 32, 64]

    # Ensure the file has the right number of lines
    if len(times) != len(thread_counts):
        print("Error: The file should have exactly 7 lines, one for each thread count.")
        sys.exit(1)

    speedups = calculate_speedup(times)
    plot_speedup(speedups, thread_counts,type_of_implementation)

if __name__ == "__main__":
    main()

