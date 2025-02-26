import csv
import json
import argparse
from datetime import datetime, timezone

def update_csv_with_hr(csv_file, hr_json, updated_csv):
    # Load heart rate data from hr.json
    with open(hr_json, "r") as file:
        hr_data = json.load(file)

    # Convert heart rate timestamps to ISO 8601 format (rounded to minutes)
    hr_dict = {}
    for timestamp, value in hr_data["heartRateValues"]:
        unix_time = timestamp / 1000  # Convert ms to s
        dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
        iso_time_min = dt.strftime('%Y-%m-%dT%H:%M:00.000Z')  # Round down to the minute
        hr_dict[iso_time_min] = value  # Store heart rate in a dictionary

    # Process the CSV file
    with open(csv_file, "r", newline="") as infile, open(updated_csv, "w", newline="") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)  # Read and write header
        writer.writerow(header)
        
        # Find the index of the "Time" column dynamically
        try:
            time_col_index = header.index("Time")
        except ValueError:
            raise ValueError("Column 'Time' not found in CSV file.")
        
        # Find the index of the "heartrate" column dynamically
        try:
            hr_col_index = header.index("heartrate")
        except ValueError:
            raise ValueError("Column 'heartrate' not found in CSV file.")
        number_of_added_hr = 0
        for row in reader:
            if row and row[time_col_index]:  # Ensure the row has a timestamp
                # Round CSV timestamp down to the nearest minute
                csv_time = row[time_col_index][:16]  # Keep only "YYYY-MM-DDTHH:MM"
                rounded_csv_time = csv_time + ":00.000Z"

                if rounded_csv_time in hr_dict:
                    number_of_added_hr += 1
                    row[hr_col_index] = hr_dict[rounded_csv_time]  # Update heart rate column
                    # remove the timestamp from the dictionary to keep track of the added hr data
                    del hr_dict[rounded_csv_time]
            writer.writerow(row)
        print(f"Searching timestamps from {len(hr_dict)} heartrate data points.")
        print(f"Added approx. {int(number_of_added_hr)} heart rate data points to activity.")
    print(f"CSV file updated and saved as {updated_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update CSV file with heart rate data.")
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument("hr_json", help="Path to the heart rate JSON file")
    parser.add_argument("updated_csv", help="Path to save the updated CSV file")

    args = parser.parse_args()

    update_csv_with_hr(args.csv_file, args.hr_json, args.updated_csv)
