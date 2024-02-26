#!/usr/bin/env python3

distance=0.0
lasttime=0.0
import io,sys,time,math
import sqlite3
import RPi.GPIO as GPIO
import curses
import queue
import threading
import statistics as st
import json,os,sys

spdchars=" ▁▂▃▄▅▆▇█"

cycleq = queue.Queue()
Q_ITEM_UPDATE = 0
Q_ITEM_CLEAR = 1


SPEED_SCALE=40


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


"""
table description:

CREATE TABLE `cycles` (
	`epochtime`	REAL(64),
	`cycletime`	timestamp,
	`dt`	REAL(64),
	`speed_mph`	REAL(64),
        `distance` REAL(64),
	PRIMARY KEY(`epochtime`)
);
"""

GPIO.setmode(GPIO.BCM)

def tf(fmt,unixtime):
    return  time.strftime(fmt,time.localtime(unixtime))

def log(x):
    now=time.time()
    open("debug.log","a").write(tf("%Y-%m-%d %H:%M:%S",now)+f"{int(math.fmod(now,1.0)*1000):03d}: {x}\n")



def doSqlInsert(thistime, lasttime, speed, distance):

    con = sqlite3.connect("cycle.db")
    sql = '''INSERT INTO cycles ( `epochtime`, `cycletime`, `dt`, `speed_mph`, `distance`) 
        VALUES (?,?,?,?,?);'''
    cur = con.cursor()
    cur.execute(sql, (thistime, tf('%Y-%m-%d %H:%M:%S',thistime), thistime-lasttime, speed, distance))
    con.commit()
    con.close()

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

lastq = 0
lasti = 0
def RecvEvent(event):
    global lasti
    thistime = time.time()
    if (thistime - lasti) > 0.13:
        cycleq.put_nowait(thistime)
    lasti = thistime;

PIN=21
PINA=20
TPIN=16
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PINA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TPIN, GPIO.OUT)
GPIO.add_event_detect(PIN, GPIO.BOTH, RecvEvent)
GPIO.add_event_detect(PINA, GPIO.BOTH, RecvEvent)
running = True

kdt=None
def main(stdscr):
    global kdt
    #set up the display
    # record the screen size
    nrows,ncols = stdscr.getmaxyx()
    # define the colors for the speed in the bar chart
    def rcolor(row):
        if row>nrows/3:
            return 3
        if row>nrows/6:
            return 4
        return 2
    # enable colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i,-1)
    # initialize the speed values to plot
    ospeeds = [0] * ncols
    odistances = [0] * ncols
    ospdraw = None
    # clear screenn and start the "trip"
    stdscr.clear()
    lasttime=0
    distance=0
    running = True
    stdscr.nodelay(True)
    while running:
        # non-blocking character input read
        c=stdscr.getch()
        if c != -1:
            stdscr.addstr(0,0,f"{c}")
        if c==ord(' '):
            # space triggers an interrupt simulating a rotation detection event
            GPIO.output(TPIN,GPIO.HIGH)
            time.sleep(0.01)
            GPIO.output(TPIN,GPIO.LOW)
        if c==ord('q'):
            # q for quit
            open("quit.flag","w").write("quit")
            return
        # pop next event from queue if there is one
        try:
            thistime = cycleq.get_nowait()
        except queue.Empty:
            if lasttime > 0:
                if time.time()-lasttime > 15:
                    # kick it
                    sys.exit(0)
            continue
        # if there is a last time....
        if lasttime == 0:
            lasttime=thistime
            continue
        else:
            # compute dt since last time
            dt = thistime - lasttime
            # if it's too short a time, it's noise or multiple pulses from the same close pass of the magnet
            if dt < 1/SPEED_SCALE:
                # too short, kick it
                lasttime=thistime
                continue
            if dt > 15:
                # too long, kick it
                distance=0
                lasttime = 0
                ospeeds=[0] * ncols
                odistances = [0] * ncols
                stdscr.clear()
                sys.exit(0)
                continue
            # we're in the "just right" zone 
            # between 1/SPEED_SCALE and 15
            if kdt is None: kdt = dt
            #kddt = (kdt - dt)**2/30
            #if dt>0:
            #    kdt -= kddt
            #else:
            #    kdt += kddt

            kdt=kdt*0.40+dt*0.60
            # calculate speed
            speed = 26*3.14159*60*60/12/5280/kdt
            if ospdraw is None:
                ospdraw = [speed] * 3
            ospdraw = [speed] + ospdraw[:-1]
            speed = st.median(ospdraw)
            
            # accumulate distance
            distance = distance + 26.0*3.14159/12/5280
            # output to today's file
            fname = tf('cyclelog-%Y%m%d.csv',thistime)
            output = f"{thistime},{tf('%Y-%m-%d %H:%M:%S',thistime)},{kdt},{speed},{distance}"
            open(fname,"a").write(f"{output}\n")
            writelatest(output)
            
            x = threading.Thread(target=doSqlInsert, args=(thistime,lasttime,speed,distance))
            x.start()



            # reread the screen size in case it has changed
            nrows,ncols = stdscr.getmaxyx()
            # update screen
            stdscr.clear()
            # add speed to graph data
            ospeeds += [speed]
            odistances += [ distance ]
            # truncate if necessary
            if len(ospeeds) > ncols:
                ospeeds=ospeeds[-ncols:]
            if len(odistances) > ncols:
                odistances=odistances[-ncols:]
            if False: #for spds in range(0,ncols):
                if spds >= len(ospeeds):
                    continue
                if ospeeds[spds]==0:
                    continue
                ts =ospeeds[spds]
                nblks=ts*nrows/SPEED_SCALE
                if nblks > nrows-2:
                    nblks = nrows-2
                nbi = int(math.floor(nblks))
                nbr =  nblks-nbi
                nbr=int(math.floor(nbr*8))
                #for r in range(nrows-2,nrows-2-nbi,-1):
                milestone10 = False
                if spds > 0 and int(odistances[spds]*10) > int(odistances[spds-1]*10):
                    milestone10 = True
                spdrow = nrows-2-nbi
                if False: #for r in range(nrows-2,0,-1):
                    pcolor = curses.color_pair(rcolor(r))|curses.A_BOLD
                    pchar = ' '
                    if milestone10:
                        pchar = '|'
                        pcolor=rcolor(nrows-1)
                    else:
                        if r > spdrow and spds>=0 and spds<ncols:
                            pchar ='█'
                        else:
                            if r == nrows-2-nbi:
                                pchar = spdchars[nbr]
                    stdscr.addstr(r,spds,pchar,pcolor)
                    if milestone10:
                        dstr = f"{int(odistances[spds]*10)/10}mi"
                        dsrow = 0
                        dscol = spds-len(dstr)//2
                        if dscol+len(dstr) > ncols-1:
                            dscol = ncols-1 - len(dstr)
                        if dscol < 0: dscol=0
                        stdscr.addstr(dsrow,dscol,dstr)


                #stdscr.addstr(nrows-2-nbi,spds,'█',curses.color_pair(rcolor(r))|curses.A_BOLD)
                #stdscr.addstr(nrows-2-nbi,spds,spdchars[nbr],curses.color_pair(rcolor(nrows-2-nbi))|curses.A_BOLD)
                for i in range(0,45,5):
                    drow = nrows-2-(int(math.floor(i*nrows/SPEED_SCALE)))
                    if drow >= 0:
                        stdscr.addstr(nrows-2-(int(math.floor(i*nrows/SPEED_SCALE))),0,"-"*ncols)
                        stdscr.addstr(nrows-2-(int(math.floor(i*nrows/SPEED_SCALE))),0,f"{i} mph")
            for spds in range(ncols):
                if spds >= len(ospeeds):
                    continue
                if ospeeds[spds]==0:
                    continue
                ts =ospeeds[spds]
                nblks=ts*nrows/SPEED_SCALE
                if nblks > nrows-2:
                    nblks = nrows-2
                nbi = int(math.floor(nblks))
                nbr =  nblks-nbi
                nbr=int(math.floor(nbr*8))
                r=nrows-2-nbi
                pchar = spdchars[nbr]
                pcolor = curses.color_pair(rcolor(r))|curses.A_BOLD
                stdscr.addstr(nrows-2-nbi,spds,pchar,pcolor)
            # display current time, speed, etc.
            stdscr.addnstr(nrows-1,0,f"{tf('%H:%M:%S',thistime)} {1/kdt:1.02f}rev/s {speed:-2.02f}mph d={distance:02.03f} {cycleq.qsize()}",ncols)
        lasttime = thistime
        stdscr.refresh()

curses.wrapper(main)
