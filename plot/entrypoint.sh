#!/bin/sh -l

set -e

cat $1 | ./kurobako plot curve -o ./output/

imagepath=$(ls ./output/*.png | head -1)

echo ::set-output name=image-path::$imagepath
