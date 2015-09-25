#!/usr/bin/env sh
# This script downloads the SUN2012 data and unzips it.

# do not change this name
dataset_dir="sun2012pascalformat"

# if you have already had the same version of dataset, you can 
# create soft link like this:
# >> ln -s <path/to/SUN2012pascalformat/> sun2012pascalformat

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget http://groups.csail.mit.edu/vision/SUN/releases/SUN2012pascalformat.tar.gz

echo "Unzipping..."

mkdir $dataset_dir
tar -zxvf SUN2012pascalformat.tar.gz && rm -f SUN2012pascalformat.tar.gz
mv SUN2012pascalformat/* $dataset_dir && rm -rf SUN2012pascalformat

ls JPEGImages > filelist.txt

echo "Done."
