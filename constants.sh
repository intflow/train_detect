#!/bin/bash

declare -A ckpt_link_map
declare -A ckpt_name_map
declare -A config_filename_map

ckpt_link_map["mobilenet_v1_ssd"]="http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_quantized_300x300_coco14_sync_2018_07_18.tar.gz"
ckpt_link_map["mobilenet_v2_ssd"]="http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03.tar.gz"

ckpt_name_map["mobilenet_v1_ssd"]="ssd_mobilenet_v1_quantized_300x300_coco14_sync_2018_07_18"
ckpt_name_map["mobilenet_v2_ssd"]="ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03"

config_filename_map["mobilenet_v1_ssd-true"]="pipeline_mobilenet_v1_ssd_retrain_whole_model.config"
config_filename_map["mobilenet_v1_ssd-false"]="pipeline_mobilenet_v1_ssd_retrain_last_few_layers.config"
config_filename_map["mobilenet_v2_ssd-true"]="pipeline_mobilenet_v2_ssd_retrain_whole_model.config"
config_filename_map["mobilenet_v2_ssd-false"]="pipeline_mobilenet_v2_ssd_retrain_last_few_layers.config"


INPUT_TENSORS='normalized_input_image_tensor'
OUTPUT_TENSORS='TFLite_Detection_PostProcess,TFLite_Detection_PostProcess:1,TFLite_Detection_PostProcess:2,TFLite_Detection_PostProcess:3'

TF_BASE="/works/tensorflow/models/research"
WORK_DIR="$PWD"
LEARN_DIR="${WORK_DIR}/learn"
DATA_DIR="/DL_data/pig500_20200303_sungil"
TFREC_DIR="${LEARN_DIR}/tfrecord"
CKPT_DIR="${LEARN_DIR}/ckpt"
TRAIN_DIR="${LEARN_DIR}/train"
OUTPUT_DIR="${LEARN_DIR}/models"

#The Last few layers
NUM_TRAINING_STEPS=500
NUM_EVAL_STEPS=100

#Whole Training
##NUM_TRAINING_STEPS=50000
##NUM_EVAL_STEPS=2000

