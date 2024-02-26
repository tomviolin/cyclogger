#!/bin/bash
echo "CYCLOLOGGER";
cd `dirname $0`
while [ ! -f quit.flag ]; do
	./cyclogger.py
	./syncdata.sh
done
rm quit.flag
