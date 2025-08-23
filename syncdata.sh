#!/bin/bash
cd `dirname $0`
rsync -av ./ optiplex:cyclo-v`date +%m-%d`
