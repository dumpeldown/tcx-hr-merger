import csv
import argparse
import numpy as np
from datetime import datetime
from scipy.interpolate import CubicSpline

def interpolate_hr(updated_csv, final_csv):
    # Read CSV and collect data
    rows = []
    timestamps = []
    heart_rates = []

    with open(updated_csv, "r", newline="") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read header
        rows.append(header)  # Store header
        
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

        for row in reader:
            rows.append(row)
            timestamps.append(row[time_col_index])  # Store timestamp
            heart_rates.append(None if row[hr_col_index] == '' else int(float(row[hr_col_index])))  # Convert HR to int or None

    # Convert timestamps to seconds
    time_seconds = np.array([
        datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() for t in timestamps
    ])

    # Filter known HR values and corresponding times
    known_indices = [i for i, hr in enumerate(heart_rates) if hr is not None]
    
    if len(known_indices) < 4:
        raise ValueError("Not enough known heart rate values for cubic spline interpolation.")

    known_times = time_seconds[known_indices]
    known_heart_rates = np.array([heart_rates[i] for i in known_indices])

    # Fit cubic spline
    cs = CubicSpline(known_times, known_heart_rates, bc_type="natural")

    # Interpolate missing HR values
    number_of_missing_hr = 0
    for i in range(len(heart_rates)):
        if heart_rates[i] is None:
            heart_rates[i] = int(cs(time_seconds[i]))  # Use cubic spline interpolation
            number_of_missing_hr += 1

    # Save the final interpolated CSV
    with open(final_csv, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(rows[0])  # Write header

        for i, row in enumerate(rows[1:]):
            row[hr_col_index] = heart_rates[i]  # Update heart rate column
            writer.writerow(row)

    print(f"Interpolated {number_of_missing_hr} missing heart rate data points.")
    print(f"Final CSV file with interpolated heart rates saved as {final_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpolate missing heart rate values in a CSV file using Cubic Spline.")
    parser.add_argument("updated_csv", help="Path to the input updated CSV file")
    parser.add_argument("final_csv", help="Path to save the final interpolated CSV file")

    args = parser.parse_args()

    interpolate_hr(args.updated_csv, args.final_csv)
