addpath('../');

global_variables;

%% Collect synthetic images according to shape list
image_list = collect_image_list(g_syn_images_folder, g_shape_list_file);

local_cluster = parcluster('local');
poolobj = parpool('local', min(g_syn_cropping_thread_num, local_cluster.NumWorkers));
fprintf('Batch cropping synthetic images from \"%s\" to \"%s\" ...\n', g_syn_images_folder, g_syn_images_cropped_folder);
batch_crop(g_syn_images_folder, g_syn_images_cropped_folder, 1, image_list);
delete(poolobj);

exit;
