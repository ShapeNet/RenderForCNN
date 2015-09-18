function get_voc12train_truncation_stats(cls, visualize, debug)

if nargin < 2
    visualize = 0;
    debug = 0;
end
if nargin < 3
    debug = 0;
end

setup_path;
    
% LOAD CAD MODELS
CADPathName = fullfile(PASCAL3D_DIR, 'CAD', [cls '.mat']);
cad = load(CADPathName);
cad = cad.(cls);

%image_dir = '/orions3-zfs/projects/rqi/Dataset/VOC12/VOCdevkit/VOC2012/JPEGImages/';
image_dir = fullfile(PASCAL3D_DIR, 'Images', [cls '_pascal']);
ids = textread(sprintf(VOCopts.imgsetpath, 'train'), '%s');


% LOGGINGS
azimuths = [];
elevations = [];
thetas = [];
distances = [];
gt_bboxes = [];
cad_bboxes = [];
gt_bboxes_draw  = [];
cad_bboxes_draw = [];
area_ratios = []; % gt bbox / cad bbox


for i = 1:numel(ids)
    if mod(i,100) == 0
        fprintf('%s: %d/%d\n', cls, i, numel(ids));
    end
    
    % Load annotation for the i'th image
    filename = fullfile(PASCAL3D_DIR, 'Annotations', sprintf('%s_pascal/%s.mat', cls, ids{i}));
    if ~exist(filename,'file')
        continue;
    end
    anno = load(filename);
    objects = anno.record.objects;
    for k = 1:length(objects)
        obj = objects(k);
        % Proceed only when the object is of cls
        if strcmp(obj.class,cls)
            bbox = obj.bbox;
            bbox_draw = [bbox(1) bbox(2) bbox(3)-bbox(1) bbox(4)-bbox(2)];
            im = imread(fullfile(image_dir, [ids{i} '.jpg']));
            % Show original image
            if debug
                imshow(im);
                hold on;
                rectangle('Position', bbox_draw, 'EdgeColor', 'g');
            end
            % Show annotated anchor points
            if debug && isfield(obj, 'anchors') == 1 && isempty(obj.anchors) == 0
                names = fieldnames(obj.anchors);
                for j = 1:numel(names)
                    if obj.anchors.(names{j}).status == 1
                        if isempty(obj.anchors.(names{j}).location) == 0
                            x = obj.anchors.(names{j}).location(1);
                            y = obj.anchors.(names{j}).location(2);
                            plot(x, y, 'ro');
                        else
                            fprintf('anchor point %s is missing!\n', names{j});
                        end
                    end
                end                
            end
            % show overlay of the CAD model
            if isfield(obj, 'cad_index') == 1 && isempty(obj.cad_index) == 0 && ...
                    isfield(obj, 'viewpoint') == 1 && isfield(obj.viewpoint, 'azimuth') == 1
                vertices = cad(obj.cad_index).vertices;
                faces = cad(obj.cad_index).faces;
                x2d = project_3d(vertices, obj);
                if isempty(x2d) == 0
                    
                    if debug
                        patch('vertices', x2d ,'faces', faces, ...
                        'FaceColor', 'blue', 'FaceAlpha', 0.2, 'EdgeColor', 'none');
                    end
                    
                    % Find bbox for the CAD model
                    bbox_cad = [min(x2d(:,1)),min(x2d(:,2)),max(x2d(:,1)),max(x2d(:,2))];
                    bbox_cad_draw = [bbox_cad(1), bbox_cad(2), bbox_cad(3)-bbox_cad(1), bbox_cad(4)-bbox_cad(2)];
                     
                    area_ratio = bbox_draw(3)*bbox_draw(4)/(bbox_cad_draw(3)*bbox_cad_draw(4));
                    if debug
                        rectangle('Position', bbox_cad_draw, 'EdgeColor','r');
                        fprintf('Approx. visible ratio: %f\n', area_ratio);
                        hold off;
                    end
                    
                    azimuths = [azimuths obj.viewpoint.azimuth];
                    area_ratios = [area_ratios area_ratio];
                    gt_bboxes = [gt_bboxes; bbox];
                    cad_bboxes = [cad_bboxes; bbox_cad];
                    gt_bboxes_draw = [gt_bboxes_draw; bbox_draw];
                    cad_bboxes_draw = [cad_bboxes_draw; bbox_cad_draw];
                end
                
            end 
            if debug
                fprintf('press button to continue...\n');
                pause();
                close all;
            end
        end
    end
end


widths = cad_bboxes(:,3) - cad_bboxes(:,1);
heights = cad_bboxes(:,4) - cad_bboxes(:,2);
r = zeros(length(azimuths), 4);
gt_cad_bboxes_diff = gt_bboxes - cad_bboxes;
r(:,1) = gt_cad_bboxes_diff(:,1) ./ widths;
r(:,3) = gt_cad_bboxes_diff(:,3) ./ widths;
r(:,2) = gt_cad_bboxes_diff(:,2) ./ heights;
r(:,4) = gt_cad_bboxes_diff(:,4) ./ heights;
left = r(:,1); top = r(:,2);
right = r(:,3); bottom = r(:,4);
mkdir(g_truncation_statistics_folder);
save(fullfile(g_truncation_statistics_folder, [cls '_truncation_stats']), 'left', 'top', 'right', 'bottom');

if visualize
    % Show relation between azimuth and area_ratios
    vnum = 8;
    azimuth_interval = [0 (360/(vnum*2)):(360/vnum):360-(360/(vnum*2))];
    ratios_by_view = zeros(vnum,1);
    for i = 1:length(azimuths)
        azimuths(i) = find_interval(azimuths(i), azimuth_interval);
    end
    for v = 1:vnum
        [tmp, index] = find(azimuths == v);
        ratios_by_view(v) = median(area_ratios(index));
    end
    figure, subplot(1,2,1), bar(ratios_by_view);
    subplot(1,2,2), scatter(azimuths, area_ratios);


    % Show hist of ratios of gt_cad_bboxes_diff/[width,height]
    figure, subplot(2,2,1), hist(left), title('left');
    subplot(2,2,2), hist(top), title('right');
    subplot(2,2,3), hist(right), title('top');
    subplot(2,2,4), hist(bottom), title('bottom');
end

function ind = find_interval(azimuth, a)
for i = 1:numel(a)
    if azimuth < a(i)
        break;
    end
end
ind = i;
if azimuth > a(end)
    ind = 1;
end
