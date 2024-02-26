#!/bin/bash

cd `dirname "$0"`
while [ \! -f stop.flag ]; do
	python3 cyclogger.py
done
rm stop.flag
