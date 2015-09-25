function test_det(prediction_folder, ARP, show_curve)
addpath(fullfile(mfilename('fullpath'), '../../'));
global_variables;

if nargin < 2
    ARP = 0;
end
if nargin < 3
    show_curve = 0;
end
if nargin < 4
    write_result = 1;
end

aps = [];
aas = [];
for k  = 1:numel(g_cls_names)
    cls = g_cls_names{k};
    try
    if ARP 
        [recall, precision, accuracy, ap, aa] = compute_recall_precision_accuracy_3dview(cls, fullfile(prediction_folder,sprintf('%s_3dview.mat',cls)), show_curve, ARP);
        aps = [aps ap];
        aas = [aas aa];
    else
        for n = [4,8,16,24]
            [recall, precision, accuracy, ap, aa] = compute_recall_precision_accuracy_azimuth(cls, n, n, fullfile(prediction_folder,sprintf('%s_v%s.mat',cls,num2str(n))), show_curve);
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


if write_result
    if ARP
        result_filename = 'arp_results.txt';
    else
        result_filename = 'avp_nv_results.txt';
    end
    fid = fopen(fullfile(prediction_folder, result_filename), 'w');
    for k = 1:N
        fprintf(fid, sprintf('%s ', g_cls_names{k}));
    end
    fprintf(fid, '\n');
    
    if ARP
        fprintf('ARP:\n');
        for k = 1:N
            fprintf(fid, sprintf('%f ', aps(k)));
        end
        fprintf(fid, '\n');
        fprintf(fid, '\n');
        fprintf(fid, 'Mean ARP = %f\n', mean(aps));
    else
        fprintf('AVP-NV (N=4,8,16,24):\n');
        for j = 1:4
            for k = 1:N
                fprintf(fid, sprintf('%f ', aps(j,k)));
            end
            fprintf(fid, '\n');
        end
        fprintf(fid, '\n');
        fprintf('Mean AVP-NV excluding bottles\n');
        avp_mean = mean(aps(:,[1,2,3,5,6,7,8,9,10,11,12]),2);
        vs = [4,8,16,24];
        for j = 1:4
            fprintf(fid, 'Mean AVP-%dV = %f\n', vs(j), mean(avp_mean(j)));
        end
    end
    fprintf(fid, '\n\n');
    fprintf(fid, 'AP:\n');
    for k = 1:N
        fprintf(fid, sprintf('%s ', g_cls_names{k}));
    end
    fprintf(fid, '\n');
    for k = 1:N
        fprintf(fid, sprintf('%f ', aas(k)));
    end
    fprintf(fid, '\n\n');
    fprintf(fid, 'Mean AP = %f\n', mean(aas));
    
    fclose(fid);
end