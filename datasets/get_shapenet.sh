#!/usr/bin/env sh
# This script downloads the ShapeNet data and unzips it.

# do not change this name
dataset_dir="shapenetcore"

# if you have already had the same version of dataset, you can 
# create soft link like this:
# >> ln -s <path/to/ShapeNetCore/> shapenetcore

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget http://shapenet.cs.stanford.edu/shapenet/obj-zip/ShapeNetCore.v1.zip

echo "Unzipping..."

mkdir $dataset_dir
unzip ShapeNetCore.v1.zip && rm -f ShapeNetCore.v1.zip
mv ShapeNetCore.v1/* $dataset_dir && rm -rf ShapeNetCore.v1
cd $dataset_dir
for zipfile in `ls *.zip`; do unzip $zipfile; done
cd ..

echo "Done."
