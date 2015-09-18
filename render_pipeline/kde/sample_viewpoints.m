function sample_viewpoints(cls, num_samples, outlier_ratio, outlier_elevation_avg, outlier_elevation_std, outlier_tilt_avg, outlier_tilt_std)
    
setup_path;

load(fullfile(g_view_statistics_folder, sprintf('%s_viewpoint_stats.mat', cls)));    
invalidSamples = find(distances == 0);

azimuths(invalidSamples) = [];
elevations(invalidSamples) = [];
tilts(invalidSamples) = [];
distances(invalidSamples) = [];    

ha = hist(azimuths, linspace(min(azimuths), max(azimuths)+1e-5, 51));
arange = linspace(min(azimuths), max(azimuths)+1e-5, 51);
ha(end) = [];

he = histc(elevations, linspace(min(elevations), max(elevations)+1e-5, 51));
erange = linspace(min(elevations), max(elevations)+1e-5, 51);
he(end) = [];

ht = histc(tilts, linspace(min(tilts), max(tilts)+1e-5, 51));
trange = linspace(min(tilts), max(tilts)+1e-5, 51);
ht(end) = [];

ha = ha / sum(ha);
he = he / sum(he);
ht = ht / sum(ht);

 % calibrate distance by a factor of 3, because estimated distances
 % from pascal3d annotations are over-estimated.
targetSamples = [azimuths', elevations', tilts', distances'/3];
bandwidth = 1.06 * std(targetSamples) * (size(targetSamples, 1)^(-0.2));

addpath(g_matlab_kde_folder);
p = kde(targetSamples', bandwidth');
newSamples = sample(p, num_samples);
rmpath(g_matlab_kde_folder);

goodSamples = newSamples';
goodSamples(:, 1) = mod(goodSamples(:, 1), 360);
goodSamples(:, 2) = mod(goodSamples(:, 2)+90, 180)-90;
goodSamples(:, 3) = mod(goodSamples(:, 3)+90, 180)-90;

distance_min = 1;
distance_max = 29;
filt = goodSamples(:, 4) > distance_max | goodSamples(:, 4) < distance_min;
goodSamples(filt, 4) = datasample(goodSamples(~filt,4), sum(filt)) + 1*rand(sum(filt),1);

% goodSamples(:, 4) = max([goodSamples(:, 4), min(distances) * ones(num_samples, 1)], [], 2);
% goodSamples(:, 4) = min([goodSamples(:, 4), max(distances) * ones(num_samples, 1)], [], 2);

% add some outliers
rp = randperm(num_samples);
numRandPerturbation = int32(num_samples*outlier_ratio);
rp = rp(1:numRandPerturbation);

randAzimuth = rand(numRandPerturbation, 1) * 360;
randElevation = max(min(normrnd(outlier_elevation_avg, outlier_elevation_std, numRandPerturbation, 1), 85),-85);
randTilt = max(min(normrnd(outlier_tilt_avg, outlier_tilt_std, numRandPerturbation, 1), 45),-45);

goodSamples(rp, 1) = randAzimuth;
goodSamples(rp, 2) = randElevation;
goodSamples(rp, 3) = randTilt;


figure,
subplot(2,2,1), hist(goodSamples(:,1), 32), title([cls ' azimuth']);
subplot(2,2,2), hist(goodSamples(:,2), 32), title([cls ' elevation']);
subplot(2,2,3), hist(goodSamples(:,3), 32), title([cls ' tilt']);
subplot(2,2,4), hist(goodSamples(:,4), 32), title([cls ' distance']);

mkdir(g_view_distribution_folder);
dlmwrite(fullfile(g_view_distribution_folder, sprintf('%s.txt', cls)), goodSamples, 'delimiter', ' ', 'precision', 6);
