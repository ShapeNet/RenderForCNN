#!/usr/bin/env sh
# This script downloads the PASCAL3D+ (release 1.1) data and unzips it.

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget http://groups.csail.mit.edu/vision/SUN/releases/SUN2012pascalformat.tar.gz

echo "Unzipping..."

mkdir sun2012pascalformat
tar -zxvf SUN2012pascalformat.tar.gz && rm -f SUN2012pascalformat.tar.gz
mv SUN2012pascalformat/* sun2012pascalformat/ && rm -rf SUN2012pascalformat

ls JPEGImages > filelist.txt

echo "Done."
