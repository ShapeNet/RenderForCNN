% add paths
RENDER4CNN_ROOT = fullfile(mfilename('fullpath'),'../../../');
PASCAL3D_DIR = fullfile(RENDER4CNN_ROOT, 'datasets/pascal3d/');
addpath(fullfile(PASCAL3D_DIR, 'VDPM'));
addpath(fullfile(PASCAL3D_DIR, 'Annotation_tools'));
addpath(RENDER4CNN_ROOT);
global_variables;

% initialize the PASCAL development kit 
tmp = pwd;
cd(fullfile(PASCAL3D_DIR, 'PASCAL/VOCdevkit'));
addpath([cd '/VOCcode']);
VOCinit;
cd(tmp);