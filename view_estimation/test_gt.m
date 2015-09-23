function test_gt(prediction_folder, view_label_folder)
% prediction_folder contains <classname>_pred_view.txt
% view_label_folder contains <classname>.txt
addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;

N = numel(g_cls_names);

acc = zeros(1,N);
mederr = zeros(1,N);

for k = 1:N
    cls = g_cls_names{k};
    try 
        [acc(k), mederr(k)] = compute_vp_acc_mederror(fullfile(prediction_folder,sprintf('%s_pred_view.txt', cls)), ...
            fullfile(view_label_folder, sprintf('%s.txt', cls)));
    catch
    end
end
display(acc);
display(mederr);
fprintf('Mean acc = %f\n', mean(acc));
fprintf('Mean mederr = %f\n (in degree)\n', mean(mederr)/pi*180);
