import sys
import re

def extract_times(file_path):
    with open(file_path, 'r') as data_file:
        data = data_file.read()

    # Regular expression to match the time format
    time_pattern =  r"Throughput\(Kops/sec\):\s*([\d\.]+)"

    # Find all matches
    matches = re.findall(time_pattern, data)

    # Write matches to txt file
    with open('times.txt', 'w') as file:
        file.write('\n'.join(matches))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py [path_to_text_file]")
        sys.exit(1)

    file_path = sys.argv[1]
    extract_times(file_path)
