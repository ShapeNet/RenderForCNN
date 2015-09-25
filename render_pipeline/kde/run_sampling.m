% Generate view samples for PASCAL3D classes
close all; clear;

setup_path;
visualize = 0;

clsList = {'aeroplane', 'bicycle', 'boat', 'bottle', 'bus', 'car', 'chair', 'diningtable', 'motorbike', 'sofa', 'train', 'tvmonitor'};


%% Collect real image statistics
for k = 1:length(clsList)
    get_voc12train_view_stats(clsList{k});
    get_voc12train_truncation_stats(clsList{k});
end

%% Visualize real image sample statistics
azimuths_all = [];
elevations_all = [];
distances_all = [];
tilts_all = [];
left_all = [];
right_all = [];
top_all = [];
bottom_all = [];
for k = 1:length(clsList)
    cls = clsList{k};
    load(fullfile(g_view_statistics_folder, sprintf('%s_viewpoint_stats.mat', cls))); 
    azimuths_all = [azimuths_all azimuths];
    elevations_all = [elevations_all, elevations];
    distances_all = [distances_all distances];
    tilts_all = [tilts_all tilts];
    if visualize
        figure, 
        subplot(2,2,1), hist(azimuths), title([cls ' azimuth']);
        subplot(2,2,2), hist(elevations), title([cls ' elevation']);
        subplot(2,2,3), hist(tilts), title([cls ' tilt']);
        subplot(2,2,4), hist(distances), title([cls ' distance']);
    end
    load(fullfile(g_truncation_statistics_folder, sprintf('%s_truncation_stats.mat', cls))); 
    left_all = [left_all, left'];
    right_all = [right_all, right'];
    top_all = [top_all, top'];
    bottom_all = [bottom_all, bottom'];
    
    if visualize
        figure,
        subplot(2,2,1), hist(left), title([cls ' left']);
        subplot(2,2,2), hist(right), title([cls ' right']);
        subplot(2,2,3), hist(top), title([cls ' top']);
        subplot(2,2,4), hist(bottom), title([cls ' bottom']);
    end
end

if visualize
    figure, 
    subplot(2,2,1), hist(azimuths_all,32), title('all azimuth');
    subplot(2,2,2), hist(elevations_all,32), title('all elevation');
    subplot(2,2,3), hist(tilts_all,32), title('all tilt');
    subplot(2,2,4), hist(distances_all,32), title('all distance');
    
    figure,
    subplot(2,2,1), hist(left_all,32), title('left all');
    subplot(2,2,2), hist(right_all,32), title('right all');
    subplot(2,2,3), hist(top_all,32), title('top all');
    subplot(2,2,4), hist(bottom_all,32), title('bottom all');
end

%% KDE on real image samples and Generate samples from estimated distributions
tilt_avg = mean(tilts_all);
tilt_std = 20;
elevation_avg = mean(elevations_all);
elevation_std = 20;
num_samples = 10^6;
outlier_ratio = 0.2;

for k = 1:length(clsList)
    cls = clsList{k};
    sample_viewpoints(cls, num_samples, outlier_ratio, elevation_avg, elevation_std, tilt_avg, tilt_std);
    sample_truncations(cls, num_samples, outlier_ratio);
end

