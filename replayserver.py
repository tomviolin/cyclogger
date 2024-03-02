#!/usr/bin/env python3
''' replays a workout for testing the web function. '''
import os
import time
import json

def writelatest(output):
    data = output.split(",")
    datajson = { 'epochdate':data[0],
            'date':data[1],
            'dt':data[2],
            'speed':data[3],
            'distance':data[4]
            }
    
    open("_latest.json","w").write(json.dumps(datajson))
    os.rename("_latest.json","latest.json")

ts = time.strftime("%Y%m%d")
ts="20240226"
f=f"cyclelog-{ts}.csv"

infile = open(f, "r")

thisdata = infile.readline().strip()

writelatest(thisdata)
while True:
    thisdata = infile.readline().strip()
    thisdt = float(thisdata.split(',')[2])
    if thisdt > 1.5: thisdt=1.5
    print (f"sleep {thisdt} --> {thisdata}")
    time.sleep(thisdt)
    writelatest(thisdata)

