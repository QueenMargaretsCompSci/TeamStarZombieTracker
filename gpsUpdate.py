#!/usr/bin/python

import gps
from os import system
from time import sleep

# create our gpsd socket
system("sudo killall gpsd")
system("sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock")

# connect to our gps
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# loop and update map with current lat and long
while True:
    report = session.next()
    if report['class'] == 'TPV':
        if hasattr(report, 'time'):
            gpsTime = report.time
            if hasattr(report, 'lon'):
                gpsLon = report.lon
                if hasattr(report, 'lat'):
                    gpsLat = report.lat
                    print("Lat = " + str(gpsLat) + " Lon = " + str(gpsLon))
                    lines = open('map.html').read().splitlines()
                    lines[17] = '\t\t\t\tvar myLat = ' + str(round(gpsLat,7)) + ';'
                    lines[18] = '\t\t\t\tvar myLng = ' + str(round(gpsLon,7)) + ';'
                    open('map.html','w').write('\n'.join(lines))
    sleep(1)
