import numpy as np
import os
import random
from tkinter.filedialog import askopenfilename,askdirectory
path = askdirectory()

#set directories
directory = path
target_directory = path + "/test"
data_set_percent_size = float(0.5)

try:
    os.makedirs(target_directory)
except FileExistsError:
    pass

#print(os.listdir(directory))

# list all files in dir that are an image
files = [f for f in os.listdir(directory) if f.endswith('.png')]

#print(files)

# select a percent of the files randomly 
random_files = random.sample(files, int(len(files)*data_set_percent_size))
#random_files = np.random.choice(files, int(len(files)*data_set_percent_size))

#print(random_files)

# move the randomly selected images by renaming directory 

for random_file_name in random_files:      
    #print(directory+'/'+random_file_name)
    #print(target_directory+'/'+random_file_name)
    os.rename(directory+'/'+random_file_name, target_directory+'/'+random_file_name)
    continue