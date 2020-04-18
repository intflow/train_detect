"""
Writer: GyeongBong Kim
Date: 23 Jan, 2020
Summary:
    - This script converts the piglet json data to for SKU11OK model. 
"""

import pickle
import json
import os

import pandas as pd
from tqdm import tqdm

## Open matching list txt file
with open('./matching_file_path.pickle', 'rb') as f:
    matching_list = pickle.load(f)

## Open each json file line by line
annotation_data = []
mapping_data = []
for idx, each_sub_list in tqdm(enumerate(matching_list)):
    # print(each_sub_list, '\n')
    meta_json_path = each_sub_list[0]
    label_json_path = each_sub_list[1]

    with open(meta_json_path, 'r', encoding="utf-8") as meta_json_tmp:
        meta_json = json.load(meta_json_tmp)

    with open(label_json_path, 'r') as label_json_tmp:
        label_json = json.load(label_json_tmp)

    #Get file_name, image_width, image_height
    file_name_tmp = meta_json['data_key']
    file_name = os.path.split(file_name_tmp)[-1]
    image_width = meta_json['image_info']['width']
    image_height = meta_json['image_info']['height']

    label_ready = label_json['result']['objects']
    for each_label_ready in label_ready:
        object_id = each_label_ready['id']
        object_class = each_label_ready['class']
        x1 = each_label_ready['shape']['box']['x']
        y1 = each_label_ready['shape']['box']['y']
        x2 = x1 + each_label_ready['shape']['box']['width']
        y2 = y1 + each_label_ready['shape']['box']['height']
        annotation_tmp = ['image/' + file_name, int(x1), int(y1), int(x2), int(y2), object_class]
        annotation_data.append(annotation_tmp)

        if object_class == 'pig_part':
            class_mapping_num = int(0)
        elif object_class == 'Pig_s':
            class_mapping_num = int(1)
        elif object_class == 'Pig_l':
            class_mapping_num = int(2)
        else:
            print('You have to check your object class again. {}'.format(object_class))
            raise ValueError

        class_mapping_tmp = [object_class, class_mapping_num]
        if not class_mapping_tmp in mapping_data:
            mapping_data.append(class_mapping_tmp)
        # mapping_data.append(class_mapping_tmp if class_mapping_tmp not in mapping_data)

df_annotation_data = pd.DataFrame(data=annotation_data, columns=['image_name', 'x1', 'y1', 'x2', 'y2', 'object_class'])
df_mapping_data = pd.DataFrame(mapping_data, columns=['class_name', 'class_ID'])

df_annotation_data.to_csv('./retinanet_type_annotation_original.csv', index=False)
df_annotation_data.to_csv('./retinanet_type_annotation.csv', index=False, header=False)

df_mapping_data.to_csv('./retinanet_type_class_mapping_original.csv', index=False)
df_mapping_data.to_csv('./retinanet_type_class_mapping.csv', index=False, header=False)