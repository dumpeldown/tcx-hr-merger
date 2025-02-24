import csv
import json
from datetime import datetime, timezone

# Load heart rate data from hr.json
with open("hr.json", "r") as file:
    hr_data = json.load(file)

# Convert heart rate timestamps to ISO 8601 format (rounded to minutes)
hr_dict = {}
for timestamp, value in hr_data["heartRateValues"]:
    unix_time = timestamp / 1000  # Convert ms to s
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    iso_time_min = dt.strftime('%Y-%m-%dT%H:%M:00.000Z')  # Round down to the minute
    hr_dict[iso_time_min] = value  # Store heart rate in a dictionary

# Process the CSV file
input_csv = "activity.csv"  # Your input CSV file
output_csv = "updated_activity.csv"

with open(input_csv, "r", newline="") as infile, open(output_csv, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header = next(reader)  # Read and write header
    writer.writerow(header)

    for row in reader:
        if row and row[0]:  # Ensure the row has a timestamp
            # Round CSV timestamp down to the nearest minute
            csv_time = row[0][:16]  # Keep only "YYYY-MM-DDTHH:MM"
            rounded_csv_time = csv_time + ":00.000Z"

            if rounded_csv_time in hr_dict:
                row[-1] = hr_dict[rounded_csv_time]  # Update heart rate column

        writer.writerow(row)

print("CSV file updated and saved as", output_csv)
