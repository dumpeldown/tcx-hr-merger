import csv
import argparse

# Function to extract the TCX header (everything before the first <Trackpoint>)
def extract_header(tcx_file):
    header_content = []
    with open(tcx_file, "r", encoding="utf-8") as file:
        for line in file:
            if "<Trackpoint>" in line:
                break
            header_content.append(line)
    return "".join(header_content)

# Function to extract the TCX footer (everything after the last </Trackpoint>)
def extract_footer(tcx_file):
    footer_content = []
    found_last_trackpoint = False
    with open(tcx_file, "r", encoding="utf-8") as file:
        for line in file:
            if "</Track>" in line:
                found_last_trackpoint = True
            if found_last_trackpoint:
                footer_content.append(line)
    return "".join(footer_content)

# Function to convert CSV data into <Trackpoint> XML format
def csv_to_tcx_trackpoints(csv_file):
    trackpoints_xml = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            trackpoint = f"""
        <Trackpoint>
            <Time>{row['Time']}</Time>
            <Position>
                <LatitudeDegrees>{row['LatitudeDegrees']}</LatitudeDegrees>
                <LongitudeDegrees>{row['LongitudeDegrees']}</LongitudeDegrees>
            </Position>
            <AltitudeMeters>{row['AltitudeMeters']}</AltitudeMeters>
            <DistanceMeters>{row['DistanceMeters']}</DistanceMeters>
            <HeartRateBpm>
                <Value>{row['heartratebpm/value']}</Value>
            </HeartRateBpm>
            <Extensions>
                <ns3:TPX xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2">
                    <ns3:Speed>{row['Speed']}</ns3:Speed>
                </ns3:TPX>
            </Extensions>
        </Trackpoint>
        """
            trackpoints_xml.append(trackpoint.strip())
    return "\n".join(trackpoints_xml)

# Main function to recreate the TCX file
def recreate_tcx(original_tcx, csv_file, output_tcx):
    header_xml = extract_header(original_tcx)
    footer_xml = extract_footer(original_tcx)
    trackpoints_xml = csv_to_tcx_trackpoints(csv_file)

    with open(output_tcx, "w", encoding="utf-8") as file:
        file.write(header_xml + "\n")  # Write header
        file.write(trackpoints_xml + "\n")  # Insert trackpoints from CSV
        file.write(footer_xml)  # Append footer

    print(f"Recreated TCX file saved as {output_tcx}")

# Argument parser for command-line execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recreate a TCX file with updated trackpoint data.")
    parser.add_argument("original_tcx", help="The original TCX file with metadata")
    parser.add_argument("csv_file", help="The CSV file with updated trackpoint data")
    parser.add_argument("output_tcx", help="The output TCX file name")

    args = parser.parse_args()
    recreate_tcx(args.original_tcx, args.csv_file, args.output_tcx)
