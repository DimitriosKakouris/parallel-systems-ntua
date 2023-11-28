import sys
import re
import glob

def extract_times(file_path):
    with open(file_path, 'r') as data_file:
        data = data_file.read()

    time_pattern = r"(?:total =\s*)([\d\.]+)s"
    matches = re.findall(time_pattern, data)

    return matches

def main():
    # Process all .out files in the current directory
    for file_path in glob.glob('run_kmeans_*.out'):
        times = extract_times(file_path)

        # Extract type of implementation from the file name
        type_of_implementation = re.search(r"run_kmeans_(.*?)\.out", file_path).group(1)

        # Create a corresponding times.txt file
        with open(f'times_{type_of_implementation}.txt', 'w') as file:
            for time in times:
                file.write(time + '\n')

if __name__ == "__main__":
    main()

