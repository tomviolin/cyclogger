= Raspberry Pi Excercycle Logger

*now featuring FLAPPY BIRD web client*



This runs on a Raspberry Pi. It uses a Hall effect magnetic field sensor which detects a small fragment of
a rare earth magnet duct-taped to the reflector on a stationary bike I use for excercise in the winter.  

The Hall sensor allows a program on the Pi (`cyclogger.py`) to record the timing of the pulses to calculate
speed and etc.  Speeds are estimated assuming a 26-inch wheel.

Timings and estimated speed are recorded to daily csv files as well as a sqlite3 database.
There is also code in there for a rudimentary ncurses display of speed vs. time. It is now disabled in favor
of a web interface which is much easier to read.

In support of the web interface, I created a program (`websocketserver.py`) which serves the data in real time via a websocket
server.  The data is transferred via an extremely primitive file interface.  Every pulse record received by
the `cyclogger.py` program is immediately written the the file `_latest.json`, which it (atomically) renames to
`latest.json`.  Any client program can read the `latest.json` to get the latest available data.  Recall that when
a file in a Linux filesystem is deleted, while it is removed from the directory, the open file is actually kept intact
as long as any processes still have the file open. This allows client programs to retrieve an updated copy of the
latest available data, with no danger of having the data in the file drop out of existence while a client is reading the content.

Finally, the `www/index.html` and `www/anim-index.html` files are two versions of a web page interface.
Both programs are similar. The `index.html` file is basically a predecessor to the `index.html` file.  

Both programs open a connection to the websocket server and wait for data to arrive asynchronously over the
web socket. Upon arrival of the data packets, they update a client-side HTML5-Canvas based graph created using `Chartjs`.

The anim-index.html file is a more updated version, that includes horizontal smooth scrolling using a
Kalman easing algorithm that can adapt to a range of speeds.  I forked it from the earlier version in case it
took me more than 24 hours to get the new version going.  No excuse to miss a workout, I could use the older non-animated
version until the new version was ready.

Note however, that the web socket server can only serve one browser session at a time.  Eventually i may
make the web socket server multithreaded so that it can serve more than one session.  This functionality
is obviously limited by the resources of the Pi. In addition, I don't forsee anyone else but myself having 
much interest in watching the data from my workouts on their screens in real time, so it's not a high priority.

The real-time line/area chart scrolls from right to left, and shows a graphical record of your speed as if 
recorded by a pen plotter onto paper.

I also, for testing, created a program (replaycycledata.py) that reads in the csv from today's workout
and replays it in the same speed as it was originally recorded, by writing to the `latest.json` in the the same
threadsafe manner as the cyclogger.py program does.  This allowed me to spend some time testing the
web application, including timing-related issues, on actual data that I collected today.

The program is hard-coded to only read today's file.  This is so when I get up in the morning, I am
forced to create my own data for testing.  No getting around the workout!

