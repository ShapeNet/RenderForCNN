## Render for CNN: *Viewpoint Estimation in Images Using CNNs Trained with Rendered 3D Model Views*
Created by <a href="http://ai.stanford.edu/~haosu/" target="_blank">Hao Su</a>, <a href="http://web.stanford.edu/~rqi/" target="_blank">Charles R. Qi</a>, <a href="http://web.stanford.edu/~yangyan/" target="_blank">Yangyan Li</a>, <a href="http://geometry.stanford.edu/member/guibas/" target="_blank">Leonidas J. Guibas</a> from Stanford University.

### Introduction

Our work was initially described in an [arXiv tech report](http://arxiv.org/abs/1505.05641) and will appear as an ICCV 2015 paper. Render for CNN is a scalable image synthesis pipeline for generating millions of training images for high-capacity models such as deep CNNs. We demonstrated how to use this pipeline, together with specially designed network architecture, to train CNNs to learn viewpoints of objects from millions of synthetic images and real images. In this repository, we provide both the rendering pipeline codes and off-the-shelf viewpoint estimator for PASCAL3D+ objects.


### License

Render for CNN is released under the MIT License (refer to the LICENSE file for details).


### Citing Render for CNN
If you find Render for CNN useful in your research, please consider citing:

    @InProceedings{Su_2015_ICCV,
        Title={Render for CNN: Viewpoint Estimation in Images Using CNNs Trained with Rendered 3D Model Views},
        Author={Su, Hao and Qi, Charles R. and Li, Yangyan and Guibas, Leonidas J.},
        Booktitle={The IEEE International Conference on Computer Vision (ICCV)},
        month = {December},
        Year= {2015}
    }

### Contents
1. [Render for CNN Image Synthesis Pipeline](#render-for-cnn-image-synthesis-pipeline)
2. [Off-the-shelf Viewpoint Estimator](#off-the-shelf-viewpoint-estimator)
3. [Testing on VOC12 val](#testing-on-voc12-val)
4. [Training your Own Models](#training-your-own-models)

###  Render for CNN Image Synthesis Pipeline

**Prerequisites**

0. Blender (tested with Blender 2.71 on 64-bit Linux). You can get it from <a href="http://www.blender.org/features/past-releases/2-71/" target="_blank">Blender website</a> for free.

1. MATLAB (tested with 2014b on 64-bit Linux). You also need to compile the external kde package in `render_pipeline/kde/matlab_kde_package` by following the `README.txt` file in that folder.

2. Datasets (ShapeNet, PASCAL3D+, SUN2012) [**not required for the demo**]. If you already have the same datasets (as in urls specified in the shell scripts) downloaded, you can build soft links to the datasets with the same pathname as specified in the shell scripts. Otherwise, just do the following steps under project root folder:
	
    <pre>
    bash dataset/get_shapenet.sh
    bash dataset/get_sun2012pascalformat.sh
    bash dataset/get_pascal3d.sh
    </pre>
    
**Set up paths**

All data and code paths should be set in `global_variables.py`. We have provided you an example version `global_variables.py.example`. You only need to copy or rename the example file and **modify the Blender and MATLAB path** in it (in default the paths are set to `blend` and `matlab`). All other paths are relative to the project root folder and should be fine.

	cp global_variables.py.example global_variables.py
    
After setting Blender and MATLAB paths in `global_variables.py`, run script to set up MATLAB global variable file.

	python setup.py

#### Demo of synthesis pipeline
This small demo at `demo_render` shows how we get cropped, background overlaid images of objects from a 3D model. It also helps verity that you have all enviroment set up. To run the demo, cd into project root folder and follow steps below.

	cd demo_render
	python run_demo.py

#### Running large scale synthesis

0. **Estimate viewpoint and truncation distributions** with KDE (kernal density estimation). If you haven't compiled the kde package, go to `render_pipeline/kde/matlab_kde_package/mex`, open MATLAB and run `makemex` in MATLAB to generate mex files.
	
    <pre>
    cd render_pipeline/kde
    </pre>
    
    Open MATLAB and run the following command (expect to see plots popping up). Viewpoint and truncation statistics will be saved to `data/view_statistics` and `data/truncation_statistics`. Samples generated from estimated distrubtion will be saved to `data/view_distribution` and `truncation_distribution`.
    
    <pre>
    run_sampling;
    </pre>
    
1. **Render images with Blender** This step is computationally heavy and may take a long time depending how powerful your computers are. It takes us around 8 hours to render 2.4M images on 6 multi-core servers. If you have multiple servers with shared filesystem, you can set `g_hostname_synset_idx_map` in `global_variables.py` accordingly. Note that currently models are directly from ShapeNet, deformed models will be released separately later. 
    
    <pre>
    python render_pipeline/run_render.py
    </pre>
    
    You can stop rendering at any time and execute following commands to crop and overlay background on images that have already been rendered. In default, rendered images will be saved at `data/syn_images`.

2. **Crop images** This step is IO heavy and it takes around 1~2 hours on a multi-core server. SSD or high-end HDD disk could help a lot. In default, cropped images are saved to `data/syn_images_cropped`.
    
    <pre>
    python render_pipeline/run_crop.py
    </pre>
    
3. **Overlay backgrounds** Time consumption is similar to cropping step above. In default, background overlaid (also cropped from step above) images are saved to `data/syn_images_cropped_bkg_overlaid`.
   
    <pre>
    python render_pipeline/run_overlay.py
    </pre>

    If you'd like to get a file containing all synthesized image filenames and their labels (class, azimuth, elevation, tilt angles), we have some helper functions for that - just go look at `get_one_category_image_label_file` and `combine_files` in `view_estimation/data_prep_helper.py`, also refer to `view_estimation/prepare_training_data.py` for usage examples.

### Off-the-shelf Viewpoint Estimator

**Prerequisites**

0. <a href="https://github.com/BVLC/caffe" target="_blank">Caffe</a> (with pycaffe compiled). For testing we support the new caffe interface and prototxt files (which uses "layer" instead of "layers" in prototxt file). You can follow <a href="http://caffe.berkeleyvision.org/installation.html" target="_blank">this webpage</a> for installation details.

1. Download our pre-trained caffe model (~390MB). The model was trained on rendered images and VOC12 train set real images.

    <pre>
    cd caffe_models
    sh fetch_model.sh
    </pre>

**Set up paths**

The steps are the same as above in Render for CNN Image Synthesis Pipeline.

#### Demo of 3D viewpoint estimator
This demo at `demo_view` shows how one can use our off-the-shelf viewpoint estimator. To estimate viewpoint of an example image of airplane, do the following.

    cd demo_view
    python run_demo.py

To visualize the estimated 3D viewpoint, run and see a rendered image of the viewpoint.

    python run_visualize_3dview.py


### Testing on VOC12 val

**Prerequisites**

0. Caffe with python interface and pretrained caffe mdoel - as in requirement in [Off-the-shelf Viewpoint Estimator](#off-the-shelf-viewpoint-estimator).

1. PASCAL3D+ dataset - if you haven't downloaded it. It will be used for preparing test images and evaluation.
    
    <pre>
    bash dataset/get_pascal3d.sh
    </pre>

2. MATLAB for preparing test images.

**Set up paths**

The steps are the same as above in Render for CNN Image Synthesis Pipeline.

#### Evaluation of AVP-NV, Acc-pi/6 and MedErr
For AVP-NV (Average Viewpoint Precision), both localization (from R-CNN) and viewpoint estimation (azimuth) are evaluated. For Acc-\pi/6 and MedErr, we evaluate on VOC12 val images without truncations and occlusions. For more details on definition of the metrics, please refer to the paper.

Firstly, we need to prepare the testing images from VOC12, by running:

    python view_estimation/prepare_testing_data.py

Then, do evaluation by running:

    python view_estimation/run_evaluation.py

Results are displayed on screen and saved to `view_estimation/avp_test_results/avp_nv_results.txt` and `view_estimation/vp_test_results/acc_mederr_results.txt`

### Training your Own Models
For Caffe, go to <a href='https://github.com/charlesq34/caffe-render-for-cnn' target='_blank'>caffe-render-for-cnn</a> for the version with special loss layers (in view_prediction branch).

To prepare training data, run the script below. This will genereate LMDB in the data folder.

    python view_estimation/prepare_training_data.py
   
To do the training, modify prototxt files in the `train` folder.

You can directly download synthetic images rendered by us at https://shapenet.cs.stanford.edu/media/syn_images_cropped_bkg_overlaid.tar

We name images in this package by their viewpoints. An example is the following: 

synsetid_modelmd5_a010_e007_t016_d002.png

where azimuth angle is 10 degree, elevation angle is 7 degree. 

NOTE: The tilt angle should be flipped as to what is written in the filename. Here the tilt angle should be -16 (344) degree to make it consistent with PASCAL3D annotation.



