import argparse
import subprocess

def run_script(script, *args):
    """Helper function to execute Python scripts with arguments."""
    command = ["python", script] + list(args)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}: {result.stderr}")
        exit(1)
    print(result.stdout)

def main(original_tcx, hr_json, output_tcx):
    # Define intermediate files
    csv_file = "activity.csv"
    updated_csv = "updated_activity.csv"
    final_csv = "final_activity.csv"

    print("\n### Step 1: Converting TCX to CSV ###")
    run_script("tcx2csv.py", original_tcx, csv_file)

    print("\n### Step 2: Adding Heart Rate Data ###")
    run_script("addHR2csv.py", csv_file, hr_json, updated_csv)

    print("\n### Step 3: Interpolating Missing Heart Rate Data ###")
    run_script("interpHR.py", updated_csv, final_csv)

    print("\n### Step 4: Converting CSV Back to TCX ###")
    run_script("csv2tcx.py", original_tcx, final_csv, output_tcx)

    print(f"\n### Done! Final TCX file saved as {output_tcx} ###")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add heart rate data to a TCX file.")
    parser.add_argument("original_tcx", help="The original TCX file")
    parser.add_argument("hr_json", help="The heart rate JSON file")
    parser.add_argument("output_tcx", help="The final output TCX file")

    args = parser.parse_args()
    main(args.original_tcx, args.hr_json, args.output_tcx)
