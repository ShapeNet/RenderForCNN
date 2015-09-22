function prepare_voc12_imgs(img_set, output_img_dir, opts)
% PREPARE_VOC12_IMGS
%   prepare voc12 images (cropped from ground truth bboxes with jittering)
% input:
%   img_set: 'train' or 'val'
%   output_img_dir: output folder names, final structure is <output_img_dir>/<category>/<imgs>
%   opts: matlab struct with flip, aug_n, jitter_IoU, difficult, truncated, occluded fields
%       if flip is 1, images will be flipped. 
%       if ang_n>1, images will be augmented by jittering bbox. jitter_IoU==1 means normal crop
%       difficult, truncated, occluded \in {0,1}, where 0 indicated that we do not 
%           want images with that property (e.g. 0,0,0 means we want easy images only)
% output:
%   cropped images according to ground-truth bounding boxes (with jittering) and image filelists
%

addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;
cls_names = g_cls_names;

% paths
annotation_path = fullfile(g_pascal3d_root_folder, 'Annotations');
image_path = fullfile(g_pascal3d_root_folder, 'Images');
addpath(fullfile(g_pascal3d_root_folder, 'VDPM'));
addpath(fullfile(g_pascal3d_root_folder, 'PASCAL/VOCdevkit/VOCcode'));

% read ids of train/val set images
VOCinit;
ids = textread(sprintf(VOCopts.imgsetpath, img_set), '%s');
M = numel(ids);

% avoid duplication
assert(exist(output_img_dir,'dir')==0);
mkdir(output_img_dir);
for cls_idx = 1:numel(cls_names)
    mkdir([output_img_dir '/' cls_names{cls_idx}]);
end


for cls_idx = 1:numel(cls_names)
    cls = cls_names{cls_idx};
    labelfile = fopen(fullfile(output_img_dir, sprintf('%s.txt',cls)),'w');
     
    for i = 1:M
        if mod(i,100) == 0
            fprintf('%s: %d/%d\n', cls, i, M);
        end
        
        anno_filename = fullfile(annotation_path, sprintf('%s_pascal/%s.mat', cls, ids{i}));
        if ~exist(anno_filename,'file')
            continue;
        end
        anno = load(anno_filename);
        objects = anno.record.objects;

        for k = 1:length(objects)
            obj = objects(k);
            
            if ~isempty(obj.viewpoint) && strcmp(obj.class, cls)
                try
                    % write view annotation
                    azimuth = mod(round(obj.viewpoint.azimuth), 360);
                    elevation = mod(round(obj.viewpoint.elevation), 360);
                    tilt = mod(round(obj.viewpoint.theta), 360);
                    truncated = obj.truncated;
                    occluded = obj.occluded;
                    difficult = obj.difficult;
                    % skip un-annotated image
                    if azimuth == 0 && elevation == 0 && theta == 0
                        fprintf('skip %s...', ids{i});
                        continue;
                    end
                    % skip unwanted image
                    if (difficult==1 && opts.difficult==0) || (truncated==1 && opts.truncated==0) || (occluded==1 && opts.occluded==0)
                        fprintf('fliter skip %s...', ids{i});
                        continue;
                    end
                    
                    img_filename = fullfile(image_path, sprintf('%s_pascal/%s.jpg', cls, ids{i}));
                    im = imread(img_filename);
                    box = obj.bbox;
                    w = box(3)-box(1)+1;
                    h = box(4)-box(2)+1;
                    rect = [box(1),box(2), w, h];
                    
                    for aug_i = 1:opts.aug_n
                        % write cropped img
                        if aug_i == 1
                            cropped_im = imcrop(im, rect);
                        else
                            cropped_im = jitter_imcrop(im, rect, opts.jitter_IoU);
                        end
                        cropped_im_filename = sprintf('%s/%s/%s_%s_%s_%s.jpg', output_img_dir, cls, cls, ids{i}, num2str(k), num2str(aug_i)); 
                        imwrite(cropped_im, cropped_im_filename);
                        fprintf(labelfile, '%s %d %d %d %d\n', cropped_im_filename, cls_idx-1, azimuth, elevation, tilt);                    
                        if opts.flip
                            cropped_im_flip = fliplr(cropped_im); % flip the image horizontally
                            cropped_im_flip_filename = sprintf('%s/%s/%s_%s_%s_%s_%s.jpg', output_img_dir, cls, cls, ids{i}, num2str(k), num2str(aug_i), 'flip');
                            imwrite(cropped_im_flip, cropped_im_flip_filename);
                            fprintf(labelfile, '%s %d %d %d %d\n', cropped_im_flip_filename, cls_idx-1, mod(360-azimuth,360), elevation, mod(-1*tilt,360));                    
                        end
                    end
                catch
                end
            end
        end
    end
    fclose(labelfile);
end


