#!/usr/bin/env python3
''' replays a workout for testing the web function. '''
import os,sys
import time
import json
import glob

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
f=f"cyclelog-{ts}.csv"
if len(sys.argv)>1:
    f=sys.argv[1]
if not os.path.exists(f):
    fnames = sorted(glob.glob("cyclelog-2*.csv"))
    f=fnames[-1]

print (f"playing back {f}...")

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

