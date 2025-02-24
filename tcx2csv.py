import re
import argparse
import xml.etree.ElementTree as et

def main(input, output):
    tree = et.parse(input)
    root = tree.getroot()
    
    m = re.match(r'^({.*})', root.tag)
    ns = m.group(1) if m else ''
    
    if root.tag != ns + 'TrainingCenterDatabase':
        print('Unknown root found: ' + root.tag)
        return
    
    activities = root.find(ns + 'Activities')
    if not activities:
        print('Unable to find Activities under root')
        return
    
    activity = activities.find(ns + 'Activity')
    if not activity:
        print('Unable to find Activity under Activities')
        return
    
    columnsEstablished = False
    
    for lap in activity.iter(ns + 'Lap'):
        if columnsEstablished:
            fout.write('New Lap\n')
        
        for track in lap.iter(ns + 'Track'):
            if columnsEstablished:
                fout.write('New Track\n')
            
            first_trackpoint = True  # Flag to skip the first trackpoint

            for trackpoint in track.iter(ns + 'Trackpoint'):
                if first_trackpoint:
                    first_trackpoint = False
                    continue  # Skip the first trackpoint
                
                try:
                    time = trackpoint.find(ns + 'Time').text.strip()
                except:
                    time = ''
                try:
                    latitude = trackpoint.find(ns + 'Position').find(ns + 'LatitudeDegrees').text.strip()
                except:
                    latitude = ''
                try:
                    longitude = trackpoint.find(ns + 'Position').find(ns + 'LongitudeDegrees').text.strip()
                except:
                    longitude = ''
                try:
                    altitude = trackpoint.find(ns + 'AltitudeMeters').text.strip()
                except:
                    altitude = ''
                try:
                    bpm = trackpoint.find(ns + 'HeartRateBpm').find(ns + 'Value').text.strip()
                except:
                    bpm = ''
                try:
                    distance = trackpoint.find(ns + 'DistanceMeters').text.strip()
                except:
                    distance = ''
                try:
                    extensions = trackpoint.find(ns + 'Extensions')
                    if extensions is not None:
                        tpx = extensions.find('.//ns3:TPX', {'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'})
                        if tpx is not None:
                            speed = tpx.find('ns3:Speed', {'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'}).text.strip()
                        else:
                            speed = ''
                    else:
                        speed = ''
                except:
                    speed = ''

                if not columnsEstablished:
                    fout = open(output, 'w')
                    fout.write(','.join(('Time', 'LatitudeDegrees', 'LongitudeDegrees', 'AltitudeMeters', 'heartrate', 'DistanceMeters', 'Speed')) + '\n')
                    columnsEstablished = True
                
                fout.write(','.join((time, latitude, longitude, altitude, bpm, distance, speed)) + '\n')

    fout.close()
    print(f"Original TCX file converted to CSV format as {output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert from TCX to CSV.')
    parser.add_argument('input', help='input TCX file')
    parser.add_argument('output', help='output CSV file')
    args = parser.parse_args()
    
    main(args.input, args.output)
