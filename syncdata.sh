#!/bin/bash
cd `dirname $0`
rsync -av ./ 192.168.1.41:cyclo-v`date +%m-%d`
