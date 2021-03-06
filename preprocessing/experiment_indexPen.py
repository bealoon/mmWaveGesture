import os
import pickle

import numpy as np
from utils.path_utils import radar_data_grapher_volumned, generate_path

specimen_list = {
    generate_path('zr', 0), generate_path('zr', 1),
    #generate_path('zy', 0), generate_path('zy', 1), generate_path('zy', 2),generate_path('zy', 3)


    #generate_path('zl', 0),generate_path('zl', 1),generate_path('zl', 2),generate_path('zl', 3)
    #generate_path('py', 0),#generate_path('py', 3)
    generate_path('py', 1),generate_path('py', 2)


    #Problematic Samples:
    #generate_path('ya', 0), generate_path('ya', 2),#generate_path('ya', 1),generate_path('ya', 3),
}

# use data augmentation

isDataGen = True

for i, path in enumerate(specimen_list):
    # generate orignial data
    print('Processing specimen #' + str(i) + '__________________________________')
    radar_data_grapher_volumned(path, is_plot=True, isCluster=True, isDataGen=isDataGen)
    radar_data_grapher_volumned(path, isCluster=True, augmentation=['trans'], isDataGen=isDataGen)
    radar_data_grapher_volumned(path, isCluster=True, augmentation=['rot'], isDataGen=isDataGen)
    radar_data_grapher_volumned(path, isCluster=True, augmentation=['scale'], isDataGen=isDataGen)

    radar_data_grapher_volumned(path, isCluster=True, augmentation=['trans', 'rot'], isDataGen=isDataGen)
    radar_data_grapher_volumned(path, isCluster=True, augmentation=['trans', 'scale'], isDataGen=isDataGen)
    radar_data_grapher_volumned(path, isCluster=True, augmentation=['rot', 'scale'], isDataGen=isDataGen)

    radar_data_grapher_volumned(path, isCluster=True, augmentation=['trans', 'rot', 'scale'], isDataGen=isDataGen)
