#!/bin/bash

source "$PWD/constants.sh"
CURRENT="$PWD"

cd  "$TF_BASE"
python ${CURRENT}/create_kitti_tf_record.py \
  --classes_to_use "pig_part,Pig_s,Pig_l" \
  --data_dir "${DATASET_DIR}" \
  --label_map_path "${DATASET_DIR}/kitti_label_map.pbtxt" \
  --output_path "${DATASET_DIR}/kitti" \
  --validation_set_size 50

mv *.tfrecord "${DATASET_DIR}/"

