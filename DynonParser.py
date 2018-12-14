import csv
import gpxpy
import gpxpy.gpx
import sys
import logging
import pint
from datetime import datetime
from fit import FitFile
from fit.files.activity import ActivityFile
from fit.messages.common import FileCreator

gpx = gpxpy.gpx.GPX()


# create FIT file
fnew = ActivityFile.create("out.fit")
fnew.append(FileCreator(software_version=666))

# unit conversion
ureg = pint.UnitRegistry()

# Create first track in our GPX:
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)

# Create first segment in our GPX track:
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

with open(sys.argv[1], mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print("GPS Alt:" + row["GPS Altitude (feet)"])
        alt = (int(row["GPS Altitude (feet)"]) * ureg.feet).to(ureg.meter)
        if row["Indicated Airspeed (knots)"]:
            print("Airspeed: " + row["Indicated Airspeed (knots)"])
            speed = float(row["Indicated Airspeed (knots)"]) * 0.514444 # converts to meters per second
        wpt_time = datetime.strptime(row["GPS Date & Time"], "%Y-%m-%d %H:%M:%S")
        print(wpt_time)
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row["Latitude (deg)"], row["Longitude (deg)"],
                                                          elevation=alt, time=wpt_time))
        line_count += 1
    print(f'Processed {line_count} lines.')

    text_file = open(sys.argv[2], "w")
    text_file.write(gpx.to_xml())
    text_file.close()




    print("Done.")
