function crop_images(src_folder, dst_folder, truncation_distr_file, single_thread)

if nargin < 4
    single_thread = 0;
end
if single_thread
    num_workers = 0;
else
    num_workers = 24;
end

image_files = rdir(fullfile(src_folder,'*/*.png'));
image_num = length(image_files);
fprintf('%d images in total.\n', image_num);
if image_num == 0
    return;
end
rng('shuffle');
truncationParameters = importdata(truncation_distr_file);
truncationParametersSub = truncationParameters(randi([1,length(truncationParameters)],1,image_num),:);

fprintf('Start croping at time %s...it takes for a while!!\n', datestr(now, 'HH:MM:SS'));
report_num = 80;
fprintf([repmat('.',1,report_num) '\n\n']);
report_step = floor((image_num+report_num-1)/report_num);
t_begin = clock;
%for i = 1:image_num
parfor(i = 1:image_num, num_workers)
    src_image_file = image_files(i).name;
    try
        [I, ~, alpha] = imread(src_image_file);       
    catch
        fprintf('Failed to read %s\n', src_image_file);
    end

    [alpha, top, bottom, left, right] = crop_gray(alpha, 0, truncationParametersSub(i,:));
    I = I(top:bottom, left:right, :);

    if numel(I) == 0
        fprintf('Failed to crop %s (empty image after crop)\n', src_image_file);
    else
        dst_image_file = strrep(src_image_file, src_folder, dst_folder);
        [dst_image_file_folder, ~, ~] = fileparts(dst_image_file);
        if ~exist(dst_image_file_folder, 'dir')
            mkdir(dst_image_file_folder);
        end
        imwrite(I, dst_image_file, 'png', 'Alpha', alpha);
    end
    
    if mod(i, report_step) == 0
        fprintf('\b|\n');
    end
end      
t_end = clock;
fprintf('%f seconds spent on cropping!\n', etime(t_end, t_begin));
end
