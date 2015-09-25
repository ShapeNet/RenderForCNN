#!/usr/bin/env sh
# This script downloads the PASCAL3D+ (release 1.1) data and unzips it.

# do not change this name
dataset_dir="pascal3d"

# if you have already had the same version of dataset, you can 
# create soft link like this:
# >> ln -s <path/to/PASCAL3D+/> pascal3d

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget ftp://cs.stanford.edu/cs/cvgl/PASCAL3D+_release1.1.zip

echo "Unzipping..."

mkdir $dataset_dir
unzip PASCAL3D+_release1.1.zip && rm -f PASCAL3D+_release1.1.zip
mv PASCAL3D+_release1.1/* $dataset_dir && rm -rf PASCAL3D+_release1.1

echo "Done."
