function test_gt(prediction_folder, view_label_folder, write_result)
% prediction_folder contains <classname>_pred_view.txt
% view_label_folder contains <classname>.txt
% write_result - if set to 1, write result to acc_mederr_results.txt in prediction_folder

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

if nargin < 3
    write_result = 1;
end
if write_result
    fid = fopen(fullfile(prediction_folder, 'acc_mederr_results.txt'), 'w');
    for k = 1:N
        fprintf(fid, sprintf('%s ', g_cls_names{k}));
    end
    fprintf(fid, '\n');
    for k = 1:N
        fprintf(fid, sprintf('%f ', acc(k)));
    end
    fprintf(fid, '\n');
    for k = 1:N
        fprintf(fid, sprintf('%f ', mederr(k)/pi*180));
    end
    fprintf(fid, '\n');
    fprintf(fid, 'Mean acc = %f\n', mean(acc));
    fprintf(fid, 'Mean mederr = %f\n (in degree)\n', mean(mederr)/pi*180);
    fclose(fid);
end
