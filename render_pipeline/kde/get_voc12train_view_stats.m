function [azimuths, elevations, distances] = get_voc12train_view_stats(cls, visualize)

if nargin < 2
    visualize = 0;
end

setup_path;

ids = textread(sprintf(VOCopts.imgsetpath, 'train'), '%s');
M = numel(ids);

azimuths = [];
elevations = [];
distances = [];
tilts = [];

for i = 1:M
    if mod(i,100) == 0
        fprintf('%s: %d/%d\n',cls,i,M);
    end
    
    filename = fullfile(PASCAL3D_DIR, 'Annotations', sprintf('%s_pascal/%s.mat', cls, ids{i}));
    if ~exist(filename,'file')
        continue;
    end
    anno = load(filename);
    objects = anno.record.objects;
    for k = 1:length(objects)
        obj = objects(k);
        if ~isempty(obj.viewpoint) && strcmp(obj.class,cls)
            try
                azimuths = [azimuths obj.viewpoint.azimuth];
                elevations = [elevations obj.viewpoint.elevation];
                tilts = [tilts obj.viewpoint.theta];
                distances = [distances obj.viewpoint.distance];
            catch
            end
        end
    %     if obj.truncated==0 && obj.occluded==0 && obj.difficult==0 && strcmp(obj.class,cls)
    %         azimuths = [azimuths obj.viewpoint.azimuth];
    %         elevations = [elevations obj.viewpoint.elevation];
    %         distances = [distances obj.viewpoint.distance];
    %         %easy_chairs{cnt} = struct('idx',i,'img',ids{i},'object',objects(k));
    %         cnt = cnt + 1;
    %     end
    end
end

mkdir(g_view_statistics_folder);
save(fullfile(g_view_statistics_folder, [cls,'_viewpoint_stats']), 'azimuths', 'elevations', 'tilts', 'distances');

if visualize
    figure, 
    subplot(2,2,1), hist(azimuths), title([cls ' azimuth']);
    subplot(2,2,2), hist(elevations), title([cls ' elevation']);
    subplot(2,2,3), hist(tilts), title([cls ' tilt']);
    subplot(2,2,4), hist(distances), title([cls ' distance']);
end
