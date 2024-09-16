import csv
import sys

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        return set(int(row[0]) for row in reader)

def compare_ports(scan_ports, ssp_ports):
    return list(scan_ports - ssp_ports)

def list_compare():
    try:
        scan_ports = read_csv('scan-ports.csv')
        ssp_ports = read_csv('ssp-ports.csv')
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found. Make sure both CSV files are in the same directory as the script.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid data in CSV files. Ensure all entries are integers.")
        sys.exit(1)

    different_ports = compare_ports(scan_ports, ssp_ports)

    if different_ports:
        print("Ports in scan-ports.csv that are not in ssp-ports.csv:")
        print(", ".join(map(str, sorted(different_ports))))
    else:
        print("All ports in scan-ports.csv are present in ssp-ports.csv.")
