import caffe
from skimage.transform import resize
import math
import numpy as np

def split_label(label):
    divide1 = 360*360*360
    divide2 = 360*360
    divide3 = 360
    class_idx = label/divide1
    tmp1 = label%divide1
    azimuth = tmp1/divide2
    tmp2 = tmp1%divide2
    elevation = tmp2/divide3
    tilt = tmp2%divide3
    base = class_idx * 360
    azimuth_label = base + azimuth
    elevation_label = base + elevation
    tilt_label = base + tilt
    return (class_idx, azimuth_label, elevation_label, tilt_label)

def get_dist(a,b,period):
    return min(abs(a-b),period-abs(a-b))


def batch_predict(gpu_index, BATCH_SIZE,  model_deploy_file, model_params_file, result_keys, img_files, resize_dim = 0): 
    # MODEL RELATED
    deploy_dir = '/orions3-zfs/projects/rqi/Data/deploy/'
    img_mean_file = deploy_dir+'imagenet_mean.npy'
    
    # INIT NETWORK

    ## OLD CAFFE CLASSIFIER VERSION
    #net = caffe.Classifier(model_deploy_file,model_params_file)
    #net.set_phase_test()
    #net.set_mode_gpu()
    #net.set_mean('data', np.load(img_mean_file))
    #net.set_raw_scale('data', 255) # absolutely necessary
    #net.set_channel_swap('data', (2,1,0)) #not necessary for gray imgs
    #net.set_device(gpu_index)
    
    # NEW CAFFE VERSION
    net = caffe.Net(model_deploy_file, model_params_file, caffe.TEST)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1)) # height*width*channel -> channel*height*width
    mean_file = np.array([104,117,123])
    transformer.set_mean('data', mean_file) #### subtract mean ####
    transformer.set_raw_scale('data', 255) # pixel value range
    transformer.set_channel_swap('data', (2,1,0)) # RGB -> BGR
    
    ## OLD CAFFE VERSION
    #net = caffe.Net(model_deploy_file, model_params_file)
    #net.set_phase_test()
    #net.set_mode_gpu()
    #net.set_device(gpu_index)
    #transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    #transformer.set_transpose('data', (2,0,1)) # height*width*channel -> channel*height*width
    #mean_file = np.array([104,117,123])
    #transformer.set_mean('data', mean_file) #### subtract mean ####
    #transformer.set_raw_scale('data', 255) # pixel value range
    #transformer.set_channel_swap('data', (2,1,0)) # RGB -> BGR

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
            if resize_dim > 0: im = resize(im, (resize_dim, resize_dim))
            input_data.append(im)
        for j in range(BATCH_SIZE - len(input_data)):
            input_data.append(im)
        inputs = input_data

        # -----------------------------------------------
        # Scale to standardize input dimensions.
        #crop_dims = np.array(net.blobs[net.inputs[0]].data.shape[2:]) 
        #image_dims = crop_dims
        #input_ = np.zeros((len(inputs),
        #                   image_dims[0],
        #                   image_dims[1],
        #                   inputs[0].shape[2]),
        #                  dtype=np.float32)
        #for ix, in_ in enumerate(inputs):
        #    input_[ix] = caffe.io.resize_image(in_, image_dims)

        ## Take center crop.
        #center = np.array(image_dims) / 2.0
        #crop = np.tile(center, (1, 2))[0] + np.concatenate([
        #    -crop_dims / 2.0,
        #    crop_dims / 2.0
        #])
        #input_ = input_[:, crop[0]:crop[2], crop[1]:crop[3], :]

        ## Classify
        #caffe_in = np.zeros(np.array(input_.shape)[[0, 3, 1, 2]],
        #                    dtype=np.float32)
        #for ix, in_ in enumerate(input_):
        #    caffe_in[ix] = transformer.preprocess(net.inputs[0], in_)
        #out = net.forward_all(**{net.inputs[0]: caffe_in})
        # -----------------------------------------------
 

        # foward pass!
        #probs = net.predict(input_data, oversample=False)
        net.blobs['data'].data[...] = map(lambda x: transformer.preprocess('data', x), input_data)
        out = net.forward()
    
        for i,key in enumerate(result_keys):
            probs = out[result_keys[i]]
            for j in range(end_idx-start_idx):
                probs_lists[i].append(np.array(np.squeeze(probs[j,:])))
    return probs_lists

