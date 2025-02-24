import csv
from datetime import datetime

input_csv = "updated_activity.csv"
output_csv = "final_activity.csv"

# Read CSV and collect data
rows = []
timestamps = []
heart_rates = []

with open(input_csv, "r", newline="") as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Read header
    rows.append(header)  # Store header

    for row in reader:
        rows.append(row)
        timestamps.append(row[0])  # Store timestamp
        heart_rates.append(None if row[-1] == '' else int(float(row[-1])))  # Convert HR to int or None

# Interpolate missing values
for i in range(len(heart_rates)):
    if heart_rates[i] is None:  # Missing heart rate
        # Find previous and next known HR values
        prev_idx = next((j for j in range(i-1, -1, -1) if heart_rates[j] is not None), None)
        next_idx = next((j for j in range(i+1, len(heart_rates)) if heart_rates[j] is not None), None)

        if prev_idx is not None and next_idx is not None:
            # Convert timestamps to seconds for interpolation
            t_prev = datetime.strptime(timestamps[prev_idx], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            t_next = datetime.strptime(timestamps[next_idx], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
            t_current = datetime.strptime(timestamps[i], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

            # Linear interpolation formula
            heart_rates[i] = int(heart_rates[prev_idx] + (heart_rates[next_idx] - heart_rates[prev_idx]) *
                                 (t_current - t_prev) / (t_next - t_prev))
        elif prev_idx is not None:
            # No future HR data, use last known HR
            heart_rates[i] = heart_rates[prev_idx]
        elif next_idx is not None:
            # No past HR data, use first known HR
            heart_rates[i] = heart_rates[next_idx]

# Save the final interpolated CSV
with open(output_csv, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(rows[0])  # Write header

    for i, row in enumerate(rows[1:]):
        row[-1] = heart_rates[i]  # Update heart rate column
        writer.writerow(row)

print("Final CSV file with interpolated heart rates saved as", output_csv)
