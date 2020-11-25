#!/bin/bash

echo "Training retinanet on cluster"
echo "------"
# Settings and variables to set for training.
backbone=resnet50
batch_size=8
multi_gpu=2
epochs=150
steps=19855


# Set other fixed variables.
# Check if job has been submitted from the right folder.
if [ ! "$LS_SUBCWD" == "$(pwd)" ]
then
  echo "Job was not submitted from folder that contains the corresponding script. Exiting!"
  exit
fi

cd ..
base_dir=$(pwd)
train_dir=$(basename $base_dir)
path_to_train_dir=$base_dir/train
#path_to_train_dir_scratch=$TMPDIR/02_TrainFiles
#path_to_data_scratch=$SCRATCH/data_regression_optical.tar
#path_to_data_dir_local_scratch=$TMPDIR/01_Data
# path_to_network_dir=$HOME/catkin_ws_rega/src/fw_human_detection_rega/dependencies/keras-retinanet
# path_to_store_snapshots=$SCRATCH/$train_dir/00_snapshots
# path_to_store_tensorboard_log=$SCRATCH/$train_dir/01_tensorboard_log
path_to_training_csv=$path_to_train_dir_scratch/retinanet_annotations_training_data.csv
path_to_classes_csv=$path_to_train_dir_scratch/retinanet_classes.csv
path_to_validations_csv=$path_to_train_dir_scratch/retinanet_annotations_validation_data.csv
# path_to_weights_dir_local_scratch=$TMPDIR/03_Weights
# path_to_init_weights=$SCRATCH/00_init_weights/$train_dir.h5
# path_to_init_weights_local_scratch=$path_to_weights_dir_local_scratch/$train_dir.h5

# Load all the modules and create the necessary directories.
echo "Loading modules"
echo "------"
module load eth_proxy
module load gcc/4.8.5
module load python_gpu/3.6.4
module load opencv/3.4.1
module load hdf5/1.10.1

echo "Creating directories"
echo "------"
if [ -d "$path_to_store_snapshots" ]
then
  echo "Snapshots folder already exists. Rename and start again. Exiting!"
  exit
else
  mkdir -p $path_to_store_snapshots
fi

if [ -d "$path_to_store_tensorboard_log" ]
then
  echo "Tensorboard log folder already exists. Rename and start again. Exiting!"
  exit
else
  mkdir -p $path_to_store_tensorboard_log
fi

mkdir -p $path_to_train_dir_scratch
mkdir -p $path_to_weights_dir_local_scratch

# Check for needed dataset.
echo "Check for dataset"
echo "------"
if [ -e "$path_to_data_scratch" ]
then
    echo "Dataset found. Continue."
else
    echo "No dataset found. Please provide/upload required dataset to SCRATCH. Exiting!"
    exit
fi

# Check for needed initializer weights in SCRATCH.
echo "Check for initializer weights in SCRATCH"
echo "------"
if [ -e "$path_to_init_weights" ]
then
    echo "Initializer weights found in SCRATCH. Continue."
else
    echo "No initializer weights found in SCRATCH. Please provide/upload required weights to SCRATCH. Exiting!"
    exit
fi

# Extract tar into local scratch folder.
echo "Extracting data into local scratch folder"
echo "------"
mkdir -p $path_to_data_dir_local_scratch
tar -xf $path_to_data_scratch -C $path_to_data_dir_local_scratch

# Copy the related training files into the local scratch folder.
echo "Copying training files into local scratch"
echo "------"
cp -a $path_to_train_dir $TMPDIR

# Copy the initializer weights.
echo "Copying initializer weights into local sratch"
echo "------"
cp -a $path_to_init_weights $path_to_weights_dir_local_scratch

# Check for needed initializer weights in TMPDIR.
echo "Check for initializer weights in TMPDIR"
echo "------"
if [ -e "$path_to_init_weights_local_scratch" ]
then
    echo "Initializer weights found in TMPDIR. Continue."
else
    echo "No initializer weights found in TMPDIR. Please provide/upload required weights to TMPDIR. Exiting!"
    exit
fi

# Change all the image paths using the local scratch directory.
echo "Changing image paths of files in local scratch folder"
echo "------"
cd $path_to_train_dir_scratch
local_scratch_path=$path_to_data_dir_local_scratch/optical
sed -i "s|/BASE_PATH|$local_scratch_path|g" retinanet_annotations_test_data.csv
sed -i "s|/BASE_PATH|$local_scratch_path|g" retinanet_annotations_training_data.csv
sed -i "s|/BASE_PATH|$local_scratch_path|g" retinanet_annotations_validation_data.csv

cd $path_to_network_dir

echo "Install deps"
echo "------"
pip install . --user
pip install --user opencv-python==3.4.1.15
pip install --user --upgrade keras
python setup.py build_ext --inplace # When running from cloned repo directly: compile cython code.

cd $path_to_network_dir/keras_retinanet/bin

echo "Start training $backbone"
echo "------"
python train.py \
--multi-gpu $multi_gpu \
--multi-gpu-force \
--random-transform \
--backbone $backbone \
--weights $path_to_init_weights_local_scratch \
--batch-size $batch_size \
--epochs $epochs \
--steps $steps \
--snapshot-path $path_to_store_snapshots \
--tensorboard-dir $path_to_store_tensorboard_log csv $path_to_training_csv $path_to_classes_csv \
--val-annotations $path_to_validations_csv
