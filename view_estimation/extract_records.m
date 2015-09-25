BASE_DIR = fullfile(mfilename('fullpath'),'../');
addpath(fullfile(BASE_DIR, '../'));
global_variables;

% viewpoint annotation path
%path_ann_view = '../Annotations';
path_ann_view = fullfile(g_pascal3d_root_folder, 'Annotations');

% read ids of validation images
addpath(fullfile(g_pascal3d_root_folder, 'VDPM'));
addpath(fullfile(g_pascal3d_root_folder, 'PASCAL/VOCdevkit/VOCcode'));
VOCinit;
%pascal_init;
ids = textread(sprintf(VOCopts.imgsetpath, 'val'), '%s');
M = numel(ids);

for i = 1:M
    % read ground truth bounding box
    rec = PASreadrecord(sprintf(VOCopts.annopath, ids{i}));
    voc12val_records{i} = rec;
end

save(fullfile(BASE_DIR, 'voc12val_records.mat'),'voc12val_records');
