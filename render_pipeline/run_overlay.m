addpath('../');

global_variables;

%% Collect synthetic images according to shape list
image_list = collect_image_list(g_syn_images_cropped_folder, g_shape_list_file);

local_cluster = parcluster('local');
poolobj = parpool('local', min(g_syn_bkg_overlay_thread_num, local_cluster.NumWorkers));
fprintf('Background overlaying \"%s\" to \"%s\" ...\n', g_syn_images_cropped_folder, g_syn_images_bkg_overlaid_folder);
background_overlay(g_syn_images_cropped_folder, g_syn_images_bkg_overlaid_folder, image_list, g_syn_bkg_filelist, g_syn_bkg_folder, g_syn_cluttered_bkg_ratio);
delete(poolobj);

exit;
