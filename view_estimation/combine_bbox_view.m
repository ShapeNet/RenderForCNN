% combine detection bbox result and viewestimation result
% if ~is3d
% input: bbox: N*5 (x1,y1,x2,y2,score), view: N*1 (view)
% output: combined: N*6 (x1,y1,x2,y2,view,score) as aeroplane_v4.mat etc.
% if is3d
% input: bbox: N*5 (x1,y1,x2,y2,score), view: N*3 (azimuth, elevation, tilt)
% output: combined: N*8 (x1,y1,x2,y2,azimuth,elevation,tilt,score) as aeroplane_3dview.mat etc.
%
% view_pred_file: each line is view for an image
% det_bbox_mat_file: .mat file with object "boxes" as Nx5 array
%
function combine_bbox_view(cls, det_bbox_mat_file, view_pred_file, output_folder, is3d)

addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;

if nargin < 5
   is3d = 0;
end

mkdir(output_folder);

for cls_idx = 1:numel(g_cls_names)
    cls = g_cls_names{cls_idx}
    try 
    object = load(det_bbox_mat_file);
    boxes = object.boxes;
    views = importdata(view_pred_file);
    if is3d
        dets = combine_bbox_3dview(boxes, views);
        save(fullfile(output_folder, sprintf('%s_3dview.mat',cls)), 'dets');
    else 
        for vnum_test = [4,8,16,24]
          azimuth_interval = [0 (360/(vnum_test*2)):(360/vnum_test):360-(360/(vnum_test*2))];
          dets = combine_bbox_azimuthview(boxes, views, azimuth_interval); 
          save(fullfile(output_folder, sprintf('%s_v%s.mat',cls, num2str(vnum_test))), 'dets');
        end
    end
    catch
      fprintf('%s error..', cls);
      continue;
    end
end


function dets = combine_bbox_azimuthview(boxes, views, azimuth_interval)
n = 1;
dets = cell(1,numel(boxes));
for k = 1:numel(boxes)
    b = boxes{k};
    d = zeros(size(b,1),6,'single');
    d(:,1:4) = b(:,1:4);
    
    for j = 1:size(b,1)
        d(j,5) = find_interval(views(n), azimuth_interval);
        n = n + 1;
    end
    
    d(:,6) = b(:,5);
    dets{k} = d;
end


function dets = combine_bbox_3dview(boxes, views)
n = 1;
dets = cell(1,numel(boxes));
for k = 1:numel(boxes)
    b = boxes{k};
    d = zeros(size(b,1),8,'single');
    d(:,1:4) = b(:,1:4);
    
    for j = 1:size(b,1)
        d(j,5:7) = views(n,:)
        n = n + 1;
    end
    
    d(:,8) = b(:,5);
    dets{k} = d;
end



function ind = find_interval(azimuth, a)

for i = 1:numel(a)
    if azimuth < a(i)
        break;
    end
end
ind = i - 1;
if azimuth > a(end)
    ind = 1;
end
