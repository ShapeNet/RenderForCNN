import caffe
from caffe.proto import caffe_pb2
import lmdb
import os
import sys
import math
import numpy as np
import argparse
from PIL import Image
from multiprocessing import Pool
import datetime
from google.protobuf import text_format
import scipy.ndimage
import skimage.transform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

'''
@brief:
    get serialized datum of image-label pair, used solely for caffe
@input:
    img_label - (img_filename, label)
@output:
    serialized datum of resized,colored,channel-swapped,transposed image
'''
def imglabel2datum(img_label):
    imname, label = img_label
    im = Image.open(imname)
    #  ** resize **
    im = im.resize((g_images_resize_dim, g_images_resize_dim), Image.ANTIALIAS)
    # convert to array
    im = np.array(im)
    # convert gray to color
    if len(np.shape(im)) == 2: # gray image
        im = im[:,:,np.newaxis]
        im = np.tile(im, [1,1,3])
    # change RGB to BGR
    im = im[:,:,::-1]
    # change H*W*C to C*H*W
    im = im.transpose((2,0,1))
    datum = caffe.io.array_to_datum(im, label)
    datum = datum.SerializeToString()
    return datum

'''
@brief:
    Image LMDB writing with parallal data serialization (which takes most time).
@input:
    image_file - txt file each line of which is image filename
    output_lmdb - lmdb pathname
@output:
    generate image LMDB (label is just idx of image in the image_file)
    labels should be separately prepared
    note: lmdb key is idx number (e.g. 0000000021) of image in image_file
'''
def write_image_lmdb(image_file, output_lmdb):
    img_filenames = [line.rstrip().split(' ')[0] for line in open(image_file, 'r')]
    N = len(img_filenames)
    
    p = Pool(20)
    batch_N = 1000
    
    in_db = lmdb.open(output_lmdb, map_size=int(1e12))
    with in_db.begin(write=True) as in_txn:
        for in_idx in range(N):
            if (in_idx % batch_N) == 0:
                print('[%s]: %d/%d' % (datetime.datetime.now(), in_idx, N))
                batch_ims = [(img_filenames[k+in_idx], k+in_idx) \
                             for k in range(min(batch_N, N-in_idx))]
                batch_datums = p.map(imglabel2datum, batch_ims)
            in_txn.put('{:0>10d}'.format(in_idx), batch_datums[in_idx % batch_N])
    in_db.close()

'''
@brief:
    Vector LMDB writing.
@input:
    input_txt_file - txt file each line is vector values separated by space
    output_lmdb - lmdb pathname
@output:
    generate vector LMDB (can be used as labels)
    note: lmdb key is idx number (e.g. 0000000021) of image in image_file
'''
def write_vector_lmdb(input_txt_file, output_lmdb):
    lines = [line.rstrip() for line in open(input_txt_file, 'r')]
    N = len(lines)
    
    in_db = lmdb.open(output_lmdb, map_size=int(1e12))
    report_N = 1000
    with in_db.begin(write=True) as in_txn:
        for in_idx in range(N):
            if (in_idx%report_N) == 0:
                print('[%s]: %d/%d' % (datetime.datetime.now(), in_idx, N))
            ll = lines[in_idx].split(' ')
            datum = np.array([float(x) for x in ll])
            datum = np.reshape(datum, [len(datum),1,1])
            datum = caffe.io.array_to_datum(datum, in_idx)
            in_txn.put('{:0>10d}'.format(in_idx), datum.SerializeToString())
    in_db.close()


'''
@brief:
    Load vectors from LMDB, return the vectors as NxD numpy array
'''
def load_vector_from_lmdb(dbname, feat_dim, max_num=float('Inf')):
    in_db = lmdb.open(dbname, map_size=int(1e12))
    print dbname, in_db.stat()

    N = min(in_db.stat()['entries'], max_num) 
    feats = np.zeros((N,int(feat_dim)))
    
    with in_db.begin(write=False) as in_txn:
        for k in range(N):
            print k
            keyname = '%010d' % k
            a = in_txn.get(keyname)
            datum = caffe_pb2.Datum()
            datum.ParseFromString(a)
            array =  caffe.io.datum_to_array(datum)
            #print array, np.shape(array)
            array = np.squeeze(array)
            assert(array is not None)
            feats[k,:] = array
    in_db.close()
    return feats

'''
@brief:
    batch caffe net forwarding.
@inpiut:
    model_deploy_file: caffe prototxt deploy file (new version using layer instead of layers)
    model_params_file: .caffemodel file
    BATCH_SIZE: depending on your GPU memory, can be as large as you want.
    result_keys: names of features (1D vector) you want to extract
    img_files: filenames of images to be tested
    mean_file: used for substraction in preprocessing of the image
    resize_dim (D): resize image to DxD
@output:
    return features in a list [<features1>, <features2>,...] of len(result_keys)
    <features1> is a list of [<nparray-feature1-of-image1>, <nparray-of-feature1-of-image2>,...] of len(img_files)
'''
def batch_predict(model_deploy_file, model_params_file, BATCH_SIZE, result_keys, img_files, mean_file, resize_dim = 0): 
    # set imagenet_mean
    if mean_file is None:
        imagenet_mean = np.array([104,117,123])
    else:
        imagenet_mean = np.load(mean_file)
        net_parameter = caffe_pb2.NetParameter()
        text_format.Merge(open(model_deploy_file, 'r').read(), net_parameter)
        print net_parameter
        print net_parameter.input_dim, imagenet_mean.shape
        ratio = resize_dim*1.0/imagenet_mean.shape[1]
        imagenet_mean = scipy.ndimage.zoom(imagenet_mean, (1, ratio, ratio))
    
    # INIT NETWORK - NEW CAFFE VERSION
    net = caffe.Net(model_deploy_file, model_params_file, caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1)) # height*width*channel -> channel*height*width
    transformer.set_mean('data', imagenet_mean) #### subtract mean ####
    transformer.set_raw_scale('data', 255) # pixel value range
    transformer.set_channel_swap('data', (2,1,0)) # RGB -> BGR

    # set test batch size
    data_blob_shape = net.blobs['data'].data.shape
    data_blob_shape = list(data_blob_shape)
    net.blobs['data'].reshape(BATCH_SIZE, data_blob_shape[1], data_blob_shape[2], data_blob_shape[3])

    ## BATCH PREDICTS
    batch_num = int(math.ceil(len(img_files)/float(BATCH_SIZE)))
    probs_lists = [[] for _ in range(len(result_keys))]
    for k in range(batch_num):
        start_idx = BATCH_SIZE * k
        end_idx = min(BATCH_SIZE * (k+1), len(img_files))
        print 'batch: %d/%d, idx: %d to %d' % (k, batch_num, start_idx, end_idx)
    
        # prepare batch input data
        input_data = []
        for j in range(start_idx, end_idx):
            im = caffe.io.load_image(img_files[j])
            if resize_dim > 0: im = skimage.transform.resize(im, (resize_dim, resize_dim))
            input_data.append(im)
        for j in range(BATCH_SIZE - len(input_data)):
            input_data.append(im)
        inputs = input_data

        # foward pass!
        net.blobs['data'].data[...] = map(lambda x: transformer.preprocess('data', x), input_data)
        out = net.forward()
    
        for i,key in enumerate(result_keys):
            probs = out[result_keys[i]]
            for j in range(end_idx-start_idx):
                probs_lists[i].append(np.array(np.squeeze(probs[j,:])))
    return probs_lists

