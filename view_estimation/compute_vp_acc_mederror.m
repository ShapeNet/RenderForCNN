function [acc, mederr] = compute_vp_acc_mederror(view_filename, img_label_filename)

est_views = importdata(view_filename);
object = importdata(img_label_filename);
data = object.data;
gt_views = data(:,2:4);

% CALCULATE ROTATION MATRIX ANGLES
est_views = est_views/180*pi;
gt_views = gt_views/180*pi;
N = size(gt_views,1);
R_angle_results = [];
for j = 1:N
   R_pred = angle2dcm(est_views(j,1), est_views(j,2), est_views(j,3));
   R_label = angle2dcm(gt_views(j,1), gt_views(j,2), gt_views(j,3));
   R_angle = norm(logm(R_pred'*R_label)) / sqrt(2);
   R_angle_results = [R_angle_results; R_angle];
end

acc = sum(R_angle_results < pi/6) / length(R_angle_results);
mederr = median(R_angle_results);

end
