import caffe
import lmdb
import numpy as np
import argparse
from PIL import Image
from multiprocessing import Pool
import datetime

'''
@brief:
    get serialized datum of image-label pair, used solely for caffe
@input:
    img_label - (img_filename, label)
    resize_dim (D) - resize image to DxD, if resize_dim is 0, no resize.
@output:
    serialized datum of resized,colored,channel-swapped,transposed image
'''
def imglabel2datum(img_label, resize_dim=0):
    imname, label = img_label
    im = Image.open(imname)
    # resize
    if resize_dim > 0:
      im = im.resize((resize_dim, resize_dim), Image.ANTIALIAS)
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
    image_resize_dim (D) - resize images to DxD
@output:
    generate image LMDB (label is just idx of image in the image_file)
    labels should be separately prepared
    note: lmdb key is idx number (e.g. 0000000021) of image in image_file
'''
def write_image_lmdb(image_file, output_lmdb, image_resize_dim):
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


