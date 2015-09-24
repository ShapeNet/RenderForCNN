#!/usr/bin/env sh
# This script downloads the ShapeNet data and unzips it.

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget http://shapenet.cs.stanford.edu/shapenet/obj-zip/ShapeNetCore.v1.zip

echo "Unzipping..."

mkdir shapenetcore
unzip ShapeNetCore.v1.zip && rm -f ShapeNetCore.v1.zip
mv ShapeNetCore.v1/* shapenetcore/ && rm -rf ShapeNetCore.v1
cd shapenetcore
for zipfile in `ls *.zip`; do unzip $zipfile; done
cd ..

echo "Done."
