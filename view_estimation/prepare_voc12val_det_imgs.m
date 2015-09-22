function prepare_voc12val_det_imgs(output_img_dir, bbox_mat_filelist, resize_dim)   
% PREPARE_VOC12VAL_DET
%   Prepare testing images from detector outputs on VOC12 val set.
% input:
%   output_img_dir: output image folder name, output will be like <output_img_dir>/<category>/<imgs>
%   bbox_mat_filenames: txt files containing a list of bbox mat filenames
%   resize_dim (D): if >0 resize images to DxD.
%

addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;
cls_names = g_cls_names;

% paths
annotation_path = fullfile(g_pascal3d_root_folder, 'Annotations');
image_path = fullfile(g_pascal3d_root_folder, 'PASCAL/VOCdevkit/VOC2012/JPEGImages');
addpath(fullfile(g_pascal3d_root_folder, 'VDPM'));
addpath(fullfile(g_pascal3d_root_folder, 'PASCAL/VOCdevkit/VOCcode'));

% read ids of train/val set images
VOCinit;
img_set = 'val';
ids = textread(sprintf(VOCopts.imgsetpath, img_set), '%s');
M = numel(ids);

bbox_mat_filenames = importdata(bbox_mat_filelist);
for k = 1:numel(bbox_mat_filenames)
    bbox_mat_filenames{k} = fullfile(g_detection_results_folder, bbox_mat_filenames{k});
end

% avoid duplication
assert(exist(output_img_dir,'dir')==0);
mkdir(output_img_dir);
for cls_idx = 1:numel(cls_names)
    mkdir([output_img_dir '/' cls_names{cls_idx}]);
end


for cls_idx = 1:numel(cls_names)
    cls = cls_names{cls_idx};
    
    imgfile = fopen(fullfile(output_img_dir, sprintf('%s.txt', cls)),'w');
    
    % load detection bboxes of all images for class
    detection_filename = bbox_mat_filenames{cls_idx};
    assert(~isempty(strfind(detection_filename, cls)));
    mat = load(detection_filename);
    det_bboxes_all = mat.boxes;
    
    for i = 1:M
        if mod(i,100) == 0
            fprintf('%s: %d/%d\n', cls, i, M);
        end
        
        % bboxes for image i, class cls
        det_bboxes = det_bboxes_all{i};
        
        % load i-th image in VOC val
        img_filename = fullfile(image_path, sprintf('%s.jpg', ids{i}));
        im = imread(img_filename);
        
        for k = 1:size(det_bboxes,1)
            box = det_bboxes(k,:);
            box = box(1:4);
            w = box(3)-box(1)+1;
            h = box(4)-box(2)+1;
            rect = [box(1),box(2), w, h];

            % write cropped img
            cropped_im = imcrop(im, rect);
            if resize_dim > 0
                copped_im = imresize(cropped_im, [resize_dim, resize_dim]);
            end
            cropped_im_filename = sprintf('%s/%s/%s_%s_%s.jpg', output_img_dir, cls, cls, ids{i}, num2str(k));
            imwrite(cropped_im, cropped_im_filename);
            fprintf(imgfile, '%s\n', cropped_im_filename);    
        end
    end
    fclose(imgfile);
end



