#!/bin/bash

cd `dirname $0`

thiscmd=`basename $0 .sh`

case $thiscmd in
startserver|restartserver)
	# make sure any old server processes are dead
	./stopserver.sh

	# start web server
	echo -n "starting web server..."
	cd www
	screen -d -m python3 -m http.server --cgi
	cd ..
	echo "OK"

	# start web socket server
	echo -n "starting websocketserver..."
	screen -d -m ./websocketserver.py
	echo "OK"

	# start cyclogger
	echo -n "starting gocycle.sh..."
	screen -d -m ./gocycle.sh
	echo "OK"

	;;

stopserver)
	# stop cyclogger
	echo "stopping cyclogger..."
	echo "processes: `pgrep -f '(gocycle.sh|cyclogger.py)'`"
	pkill -9 -f '(gocycle.sh|cyclogger.py)'

	# stop web socket server
	echo "stopping websocketserver..."
	echo "processes: `pgrep -f websocketserver`"
	pkill -9 -f websocketserver

	# stop web server
	echo "stopping http.server..."
	echo "processes: `pgrep -f http.server`"
	pkill -f http.server

	# wipe old SCREENs
	screen -wipe

	;;

serverstatus)
	# list the current SCREEN sessions
	cd /run/screen/S-$USER
	for S in *; do
		echo '======== '$S' ========'
		screen -S $S -X hardcopy /tmp/$USER-$S
		cat /tmp/$USER-$S
	done | more -s

	;;


*)
	echo "script must be named startserver.sh or stopserver.sh"
	;;

esac
