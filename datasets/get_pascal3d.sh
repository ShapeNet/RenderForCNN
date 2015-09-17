#!/usr/bin/env sh
# This script downloads the PASCAL3D+ (release 1.1) data and unzips it.

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading..."

wget ftp://cs.stanford.edu/cs/cvgl/PASCAL3D+_release1.1.zip

echo "Unzipping..."

mkdir pascal3d
unzip PASCAL3D+_release1.1.zip && rm -f PASCAL3D+_release1.1.zip
mv PASCAL3D+_release1.1/* pascal3d/ && rm -rf PASCAL3D+_release1.1

echo "Done."
