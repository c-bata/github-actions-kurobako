#!/bin/sh -l

set -e

args="-o ./output/"

if [ $2 != "false" ]; then
  args="$args --errorbar"
fi

if [ $3 != "false" ]; then
  args="$args --ylogscale"
fi

if [ $4 != "none" ]; then
  args="$args --xmin $4"
fi

if [ $5 != "none" ]; then
  args="$args --xmax $5"
fi

if [ $6 != "none" ]; then
  args="$args --ymin $4"
fi

if [ $7 != "none" ]; then
  args="$args --ymax $5"
fi

if [ $8 != "none" ]; then
  args="$args --width $8"
fi

if [ $9 != "none" ]; then
  args="$args --height $9"
fi


cat $1 | ./kurobako plot curve $args

imagepath=$(ls ./output/*.png | head -1)

echo ::set-output name=image-path::$imagepath

