#!/bin/sh -l

set -e

if [ $2 != "false" ]; then
  cat $1 | ./kurobako plot curve --errorbar -o ./output/
else
  cat $1 | ./kurobako plot curve -o ./output/
fi

imagepath=$(ls ./output/*.png | head -1)

echo ::set-output name=image-path::$imagepath
