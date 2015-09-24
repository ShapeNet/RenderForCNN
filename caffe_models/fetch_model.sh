#!/usr/bin/env sh
# This script downloads pretrained caffe model

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

FILE=render4cnn-release1-caffe-model.zip
CHECKSUM=06e35b8d4cfd6705d03a2f3b97d8edb6

if [ -f $FILE ]; then
    echo "File already exists. Checking md5..."
    os=`uname -s`
    if [ "$os" = "Linux" ]; then
        checksum=`md5sum $FILE | awk '{ print $1 }'`
    elif [ "$os" = "Darwin" ]; then
        checksum=`cat $FILE | md5`
    fi
    if [ "$checksum" = "$CHECKSUM" ]; then
        echo "Model checksum is correct. No need to download."
        exit 0
    else
        echo "Model checksum is incorrect. Need to download again."
    fi
fi

echo "Downloading precomputed viewpoint estimation caffe model (390MB)..."

wget https://shapenet.cs.stanford.edu/media/$FILE

echo "Unzipping..."

unzip $FILE

echo "Done. Please run this command again to verify that checksum = $CHECKSUM."
