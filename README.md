## Render for CNN: *Viewpoint Estimation in Images Using CNNs Trained with Rendered 3D Model Views*
Created by <a href="http://ai.stanford.edu/~haosu/" target="_blank">Hao Su</a>, <a href="http://web.stanford.edu/~rqi/" target="_blank">Charles R. Qi</a>, <a href="http://web.stanford.edu/~yangyan/" target="_blank">Yangyan Li</a>, <a href="http://geometry.stanford.edu/member/guibas/" target="_blank">Leonidas J. Guibas</a> from Stanford University.

### Introduction

Our work was initially described in an [arXiv tech report](http://arxiv.org/abs/1505.05641) and will appear as an ICCV 2015 paper. Render for CNN is a scalable image synthesis pipeline for generating millions of training images for high-capacity models such as deep CNNs. We demonstrated how to use this pipeline, together with specially designed network architecture, to train CNNs to learn viewpoints of objects from millions of synthetic images and real images. In this repository, we provide both the rendering pipeline codes and off-the-shelf viewpoint estimator for PASCAL3D+ objects.


### License

Render for CNN is released under the MIT License (refer to the LICENSE file for details).


### Citing Render for CNN
If you find Render for CNN useful in your research, please consider citing:

    @inproceedings{su2015render4cnn,
        Title={Render for CNN: Viewpoint Estimation in Images Using CNNs Trained with Rendered 3D Model Views},
        Author={Su, Hao and Qi, Charles R. and Li, Yangyan and Guibas, Leonidas J. },
        Booktitle={Computer Vision (ICCV), 2015 IEEE International Conference on},
        Year={2015},
    }

###  Render for CNN Image Synthesis Pipeline

## Prerequisites
0. Blender (tested with Blender 2.71 on 64-bit Linux)
0. MATLAB (tested with 2014b on 64-bit Linux)
0. Datasets

If you already have the same datasets (as in urls specified by .sh files below) downloaded, you can build soft links to the datasets with the same name as specified in the .sh files below.

    0. ShapeNet Dataset
    
    bash dataset/get_shapenet.sh

    0. SUN 2012 Dataset PASCAL format
    
    bash dataset/get_sun2012pascalformat.sh

    0. PASCAL3D+ Dataset

    bash dataset/get_pascal3d.sh


### Viewpoint Estimation


### Training your Own Models
