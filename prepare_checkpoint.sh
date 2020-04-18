#!/bin/bash

network_type="mobilenet_v2_ssd"
train_whole_model="false"


source "$PWD/constants.sh"

echo "PREPARING checkpoint..."
mkdir -p "${LEARN_DIR}"

ckpt_link="${ckpt_link_map[${network_type}]}"
ckpt_name="${ckpt_name_map[${network_type}]}"
cd "${LEARN_DIR}"
wget -O "${ckpt_name}.tar.gz" "$ckpt_link"
tar zxvf "${ckpt_name}.tar.gz"
mv "${ckpt_name}" "${CKPT_DIR}"

echo "CHOSING config file..."
config_filename="${config_filename_map[${network_type}-${train_whole_model}]}"
cd "${OBJ_DET_DIR}"
cp "$TF_BASE/configs/${config_filename}" "${CKPT_DIR}/pipeline.config"

echo "REPLACING variables in config file..."
sed -i "s%CKPT_DIR_TO_CONFIGURE%${CKPT_DIR}%g" "${CKPT_DIR}/pipeline.config"
sed -i "s%DATASET_DIR_TO_CONFIGURE%${DATASET_DIR}%g" "${CKPT_DIR}/pipeline.config"

##echo "PREPARING dataset"
##mkdir "${DATASET_DIR}"
##cd "${DATASET_DIR}"
##wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
##wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
##tar zxf images.tar.gz
##tar zxf annotations.tar.gz

##echo "PREPARING dataset using first two classes of Oxford-IIIT Pet dataset..."
### Extract first two classes of data
##cp "${DATASET_DIR}/annotations/list.txt" "${DATASET_DIR}/annotations/list_petsdataset.txt"
##cp "${DATASET_DIR}/annotations/trainval.txt" "${DATASET_DIR}/annotations/trainval_petsdataset.txt"
##cp "${DATASET_DIR}/annotations/test.txt" "${DATASET_DIR}/annotations/test_petsdataset.txt"
##grep "Abyssinian" "${DATASET_DIR}/annotations/list_petsdataset.txt" >  "${DATASET_DIR}/annotations/list.txt"
##grep "american_bulldog" "${DATASET_DIR}/annotations/list_petsdataset.txt" >> "${DATASET_DIR}/annotations/list.txt"
##grep "Abyssinian" "${DATASET_DIR}/annotations/trainval_petsdataset.txt" > "${DATASET_DIR}/annotations/trainval.txt"
##grep "american_bulldog" "${DATASET_DIR}/annotations/trainval_petsdataset.txt" >> "${DATASET_DIR}/annotations/trainval.txt"
##grep "Abyssinian" "${DATASET_DIR}/annotations/test_petsdataset.txt" > "${DATASET_DIR}/annotations/test.txt"
##grep "american_bulldog" "${DATASET_DIR}/annotations/test_petsdataset.txt" >> "${DATASET_DIR}/annotations/test.txt"
##
##echo "PREPARING label map..."
##cd "${OBJ_DET_DIR}"
##cp "object_detection/data/pet_label_map.pbtxt" "${DATASET_DIR}"
##
##echo "CONVERTING dataset to TF Record..."
##python object_detection/dataset_tools/create_pet_tf_record.py \
##    --label_map_path="${DATASET_DIR}/pet_label_map.pbtxt" \
##    --data_dir="${DATASET_DIR}" \
##    --output_dir="${DATASET_DIR}"
