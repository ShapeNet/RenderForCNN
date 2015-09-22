function test_det(prediction_folder, ARP=0, show_curve=0)
addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;

%show_curve = 0;
%ARP = 0;

aps = [];
aas = [];
for k  = 1:numel(g_voc12_rigid_cls_names)
    cls = g_voc12_rigid_cls_names{k};
    try
    if ARP 
        [recall, precision, accuracy, ap, aa] = compute_recall_precision_accuracy_3dview(cls, fullfile(predicition_folder,sprintf('%s_3dview.mat',cls)), show_curve, ARP);
        aps = [aps ap];
        aas = [aas aa];
    else
        for n = [4,8,16,24]
            [recall, precision, accuracy, ap, aa] = compute_recall_precision_accuracy_azimuth(cls, n, n, fullfile(predicition_folder,sprintf('%s_v%s.mat',cls,num2str(n))), show_curve);
            aps = [aps ap];
            aas = [aas aa];
        end
    end
    catch
    end
end
aas = reshape(aas, 4, numel(aas)/4);
display(aas);
aps = reshape(aps, 4, numel(aps)/4);
display(aps(1,:));
