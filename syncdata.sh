#!/bin/bash
cd `dirname $0`
rsync -av ./ optiplex:cyclo/data/cyclo-v`date +%Y-%m-%d`
