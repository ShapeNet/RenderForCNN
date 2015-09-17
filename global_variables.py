# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
g_data_folder = os.path.abspath(os.path.join(SRC_ROOT, '../data'))
g_shapenet_synset_set = ['03001627'] # chair
g_shapenet_synset_set_handle = '_'+'_'.join(g_shapenet_synset_set)
g_shape_list_file = os.path.join(g_data_folder, 'shape_list'+g_shapenet_synset_set_handle+'.txt')
g_syn_images_folder =

g_shapenet_root_folder =
g_blender_executable_path = 
g_blank_blend_file_path = 

g_shapenet_root_folder =  # shapenetcore
# ------------------------------------------------------------
# RENDER FOR CNN PIPELINE
# ------------------------------------------------------------
g_shape_synset_name_pairs = [('02691156', 'aeroplane'),
                          ('02834778', 'bicycle'),
                          ('02858304', 'boat'),
                          ('02876657', 'bottle'),
                          ('02924116', 'bus'),
                          ('02958343', 'car'),
                          ('03001627', 'chair'),
                          ('04379243', 'diningtable'), #TODO dining?
                          ('03790512', 'motorbike'),
                          ('04256520', 'sofa'),
                          ('04468005', 'train'),
                          ('03211117', 'tvmonitor')]
g_shape_synsets = [x[0] for x in g_shape_synset_name_pairs]
g_shape_names = [x[1] for x in g_shape_synset_name_pairs]
g_syn_images_num_per_category = 200000
#all_shapenet_synset_set = ['03001627' # chair
#                          ,'04379243' # table
#                          ,'03636649' # lamp
#                          ,'02958343' # car
#                          ,'02691156' # airplane
#                           ]
g_view_distribution_folder = os.path.join(g_data_folder, 'view_distribution')
g_view_distribution_files = dict(zip(g_shapenet_synsets, [os.path.join(g_view_distribution_folder, synset+'.txt') for synset in g_shapenet_synsets]))
g_syn_rendering_thread_num = 20

# render_model_views
g_syn_light_num_lowbound = 0
g_syn_light_num_highbound = 6
g_syn_light_dist_lowbound = 8
g_syn_light_dist_highbound = 20
