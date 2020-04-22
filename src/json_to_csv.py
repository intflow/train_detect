"""
Writer: GyeongBong Kim
Date: 23 Jan, 2020
Summary:
	- This script converts the piglet json data to for SKU11OK model. 
Revision:
	- 20 Apr, 2020 Support arguments to merge into jetson nano training tool-chain by K.M.Jeon	
"""

import pickle
import json
import os
import io
import argparse

import pandas as pd
from tqdm import tqdm


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', help='input data path where label and meta folders are located',
						default='.')
	parser.add_argument('--class_num', type=int, help='set number of classes in dataset',
						default=1)
	parser.add_argument('--class_list', type=str, help='set label of classes in dataset',
						default='people,dontcare')
	parser.add_argument('--gen_label_map', type=int, help='generate label_map of chosen classes',
						default=1)
	args = parser.parse_args()
	
	HOME = args.data_path
	CLASS_NUM = args.class_num
	CLASS_LABEL = args.class_list.split(',')
	GEN_LABEL_MAP = args.gen_label_map


	## Generate label_map.pbtxt
	if GEN_LABEL_MAP == 1:
		f = open(HOME+'/label_map.pbtxt', 'w')
		for i in range(CLASS_NUM):
			f.write('item {\n')
			f.write('  name: "{}"\n'.format(CLASS_LABEL[i].lower()))
			f.write('  id: {}\n'.format(i+1))
			f.write('  display_name: "{}"\n'.format(CLASS_LABEL[i].lower()))
			f.write('}\n')
	f.close()
	
	## Open matching list txt file
	with io.open(HOME+'/matching_file_path.pickle', 'rb') as f:
		matching_list = pickle.load(f)

	## Open each json file line by line
	annotation_data = []
	mapping_data = []
	for idx, each_sub_list in tqdm(enumerate(matching_list)):
		# print(each_sub_list, '\n')
		meta_json_path = each_sub_list[0]
		label_json_path = each_sub_list[1]

		with io.open(meta_json_path, 'r', encoding="utf-8") as meta_json_tmp:
			meta_json = json.load(meta_json_tmp)

		with io.open(label_json_path, 'r', encoding="utf-8") as label_json_tmp:
			label_json = json.load(label_json_tmp)

		#Get file_name, image_width, image_height
		file_name_tmp = meta_json['data_key']
		file_name = os.path.split(file_name_tmp)[-1]
		image_width = meta_json['image_info']['width']
		image_height = meta_json['image_info']['height']

		label_ready = label_json['result']['objects']
		for each_label_ready in label_ready:
			object_id = each_label_ready['id']
			object_class = each_label_ready['class'].lower()
			try:
				x1 = each_label_ready['shape']['box']['x']
				y1 = each_label_ready['shape']['box']['y']
				x2 = x1 + each_label_ready['shape']['box']['width']
				y2 = y1 + each_label_ready['shape']['box']['height']
				annotation_tmp = ['image/' + file_name, int(x1), int(y1), int(x2), int(y2), object_class]
				annotation_data.append(annotation_tmp)
			except:
				continue #Segmentation case
			
			i = 0
			while i < CLASS_NUM:
				if object_class == CLASS_LABEL[i].lower():
					class_mapping_num = int(i)
					break
				i+=1
				
			if i == CLASS_NUM:
				print('[Error]Please check your object class valid. {}'.format(object_class))
				raise ValueError
			
			class_mapping_tmp = [object_class, class_mapping_num]
			if not class_mapping_tmp in mapping_data:
				mapping_data.append(class_mapping_tmp)
			# mapping_data.append(class_mapping_tmp if class_mapping_tmp not in mapping_data)

	df_annotation_data = pd.DataFrame(data=annotation_data, columns=['image_name', 'x1', 'y1', 'x2', 'y2', 'object_class'])
	df_mapping_data = pd.DataFrame(mapping_data, columns=['class_name', 'class_ID'])

	df_annotation_data.to_csv(HOME+'/retinanet_type_annotation_original.csv', index=False)
	df_annotation_data.to_csv(HOME+'/retinanet_type_annotation.csv', index=False, header=False)

	df_mapping_data.to_csv(HOME+'/retinanet_type_class_mapping_original.csv', index=False)
	df_mapping_data.to_csv(HOME+'/retinanet_type_class_mapping.csv', index=False, header=False)
	

if __name__ == '__main__':
	main()