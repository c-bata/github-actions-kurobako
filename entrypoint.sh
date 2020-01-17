#!/bin/sh -l

set -e

python /report.py $1

time=$(date)
echo ::set-output name=time::$time
