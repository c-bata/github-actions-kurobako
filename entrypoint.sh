#!/bin/sh -l

set -e

cat $1
python /report.py $1

time=$(date)
echo ::set-output name=time::$time

