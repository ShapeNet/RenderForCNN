import os
from global_variables import *

# matlab global variable file
mf = open(os.path.join(g_render4cnn_root_folder, 'global_variables.m'), 'w')

mf.write("g_matlab_kde_folder = '%s';\n" % (g_matlab_kde_folder))
mf.write("g_view_statistics_folder = '%s';\n" % (g_view_statistics_folder))
mf.write("g_view_distribution_folder = '%s';\n" % (g_view_distribution_folder))
mf.write("g_truncation_statistics_folder = '%s';\n" % (g_truncation_statistics_folder))
mf.write("g_truncation_distribution_folder = '%s';\n" % (g_truncation_distribution_folder))

