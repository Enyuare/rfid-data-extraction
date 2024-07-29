import json
import csv
import os
import sys

def process_rfid_data(json_file_name):
    # Load the JSON data from the specified file
    with open(json_file_name, 'r') as file:
        data = [json.loads(line) for line in file]

    # Get all unique EPCs
    unique_epcs = set()
    for record in data:
        for tag in record.get('tags', []):
            unique_epcs.add(tag['epc'])

    # Prepare CSV file
    csv_file = os.path.join(os.path.dirname(json_file_name), 'extracted_rfid_data_unique_epcs.csv')

    # Create header with columns for each unique EPC's RSSI and phase
    csv_columns = ['timeStampOfRead']
    for epc in unique_epcs:
        csv_columns.append(f'{epc}_rssi')
        csv_columns.append(f'{epc}_phase')

    # Extract data
    extracted_data = []
    for record in data:
        row = {'timeStampOfRead': None}
        for tag in record.get('tags', []):
            if row['timeStampOfRead'] is None:
                row['timeStampOfRead'] = tag['timeStampOfRead']
            row[f'{tag["epc"]}_rssi'] = tag['rssi']
            row[f'{tag["epc"]}_phase'] = tag['phase']
        extracted_data.append(row)

    # Write to CSV
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in extracted_data:
            writer.writerow(data)

    print(f"Data has been written to {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_file_name>")
    else:
        json_file_name = sys.argv[1]
        process_rfid_data(json_file_name)

