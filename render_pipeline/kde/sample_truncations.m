function sample_truncations(cls, num_samples, outlier_ratio)

setup_path;
load(fullfile(g_truncation_statistics_folder, sprintf('%s_truncation_stats.mat', cls)));    

targetSamples_left_right = [left, right];
targetSamples_top_bottom = [top, bottom];
bandwidth_left_right = 1.06 * std(targetSamples_left_right) * (size(targetSamples_left_right, 1)^(-0.2));
bandwidth_top_bottom = 1.06 * std(targetSamples_top_bottom) * (size(targetSamples_top_bottom, 1)^(-0.2));

addpath(g_matlab_kde_folder);
p_left_right = kde(targetSamples_left_right', bandwidth_left_right');
p_top_bottom = kde(targetSamples_top_bottom', bandwidth_top_bottom');
newSamples_left_right = sample(p_left_right, num_samples);
newSamples_top_bottom = sample(p_top_bottom, num_samples);
rmpath(g_matlab_kde_folder);

% left, right, top, bottom.
% set up/low-bound for truncations
goodSamples = [newSamples_left_right; newSamples_top_bottom]';
filt = goodSamples(:,2) - goodSamples(:,1) > 1; % too truncated
goodSamples(filt, [1,2]) = min(max(normrnd(0, 0.1, sum(filt), 2),-0.5), 0.5);
filt = goodSamples(:,4) - goodSamples(:,3) > 1; % too truncated
goodSamples(filt, [3,4]) = min(max(normrnd(0, 0.1, sum(filt), 2),-0.5), 0.5);

% add some outliers
rp = randperm(num_samples);
numRandPerturbation = int32(num_samples*outlier_ratio);
rp = rp(1:numRandPerturbation); 
goodSamples(rp, :) = min(max(normrnd(0, 0.1, numRandPerturbation, 4),-0.5), 0.5);

figure,
subplot(2,2,1), hist(goodSamples(:,1), 32), title([cls ' left']);
subplot(2,2,2), hist(goodSamples(:,2), 32), title([cls ' right']);
subplot(2,2,3), hist(goodSamples(:,3), 32), title([cls ' top']);
subplot(2,2,4), hist(goodSamples(:,4), 32), title([cls ' bottom']);

mkdir(g_truncation_distribution_folder);
dlmwrite(fullfile(g_truncation_distribution_folder, sprintf('%s.txt', cls)), goodSamples, 'delimiter', ' ', 'precision', 6);