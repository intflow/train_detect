#!/bin/bash

source "$PWD/constants.sh"
CURRENT="$PWD"

python ./src/matching_list_maker.py --data_path $DATA_DIR
python ./src/json_to_csv.py --data_path $DATA_DIR --class_num 3 --class_list "pig_s,pig_l,pig_part"
python ./src/csv2KITTI.py --data_path $DATA_DIR
mkdir -p $DATA_DIR/kitti/image_2
mkdir -p $DATA_DIR/kitti/label_2
cp -R $DATA_DIR/img/* $DATA_DIR/kitti/image_2/
cp -R $DATA_DIR/lab_kitti_train/* $DATA_DIR/kitti/label_2/

mkdir -p $TFREC_DIR
cd  "$TF_BASE"
python ${CURRENT}/src/create_kitti_tf_record.py \
  --classes_to_use 'pig_s,pig_l' \
  --data_dir "${DATA_DIR}/kitti" \
  --label_map_path "${DATA_DIR}/label_map.pbtxt" \
  --output_path "${TFREC_DIR}" \
  --validation_set_size 50

