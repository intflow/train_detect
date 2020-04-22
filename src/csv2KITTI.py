"""
# This code convert csv label of piglet dataset to KITTI dataset format.
# KITTI dataset has been formated as follows:
# 1. 3D object detection
# ----------------------------------------------------------------------------
# Values	Name	  Description
# ----------------------------------------------------------------------------
#	1	 type		  Describes the type of object: 'Car', 'Van', 'Truck',
#					  'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
#					  'Misc' or 'DontCare'
#
#	1	 truncated	  Float from 0 (non-truncated) to 1 (truncated), where
#					  truncated refers to the object leaving image boundaries
#
#	1	 occluded	  Integer (0,1,2,3) indicating occlusion state:
#					  0 = fully visible, 1 = partly occluded
#					  2 = largely occluded, 3 = unknown
#
#	1	 alpha		  Observation angle of object, ranging [-pi..pi]
#
#	4	 bbox		  2D bounding box of object in the image (0-based index):
#					  contains left, top, right, bottom pixel coordinates
#
#	3	 dimensions	  3D object dimensions: height, width, length (in meters)
#
#	3	 location	  3D object location x,y,z in camera coordinates (in meters)
#
#	1	 rotation_y	  Rotation ry around Y-axis in camera coordinates [-pi..pi]
#
#	1	 score		  Only for results: Float, indicating confidenc
# 
# @For example
# ----------------------------------------------------------------------------
# type	truncated	occluded	alpha	bbox(x_min, y_min, x_max, y_max)	dimensions		  location		 rotation_y	  score
# ----------------------------------------------------------------------------
# Car	 0.00		   0		-1.58	587.01 173.33 614.12 200.12		  1.65 1.67 3.64   -0.65 1.71 46.70		-1.59
# Cyclist 0.00 0 -2.46 665.45 160.00 717.93 217.99 1.72 0.47 1.65 2.45 1.35 22.10 -2.35
# Pedestrian 0.00 2 0.21 423.17 173.67 433.17 224.03 1.60 0.38 0.30 -5.87 1.63 23.11 -0.03
# DontCare -1 -1 -10 650.19 175.02 668.98 210.48 -1 -1 -1 -1000 -1000 -1000 -10
# ----------------------------------------------------------------------------
#
# 2. 2D object detection
# ----------------------------------------------------------------------------
# Key	 Values		 Description
# ----------------------------------------------------------------------------
# type		1	String describing the type of object: [Car, Van, Truck, Pedestrian,Person_sitting, Cyclist, Tram, Misc or DontCare]
# truncated	1	Float from 0 (non-truncated) to 1 (truncated), where truncated refers to the object leaving image boundaries
# occluded	1	Integer (0,1,2,3) indicating occlusion state: 0 = fully visible 1 = partly occluded 2 = largely occluded 3 = unknown
# alpha		1	Observation angle of object ranging from [-pi, pi]
# bbox		4	2D bounding box of object in the image (0-based index): contains left, top, right, bottom pixel coordinates
#
# @For exmaple
# ----------------------------------------------------------------------------
# type	truncated	occluded	  alpha	  bbox(x_min, y_min, x_max, y_max)
# ----------------------------------------------------------------------------
# Pig_l		0			3			0		 468	0	577	97
# Pig_s		0			3			0		 401	143	689	260
# Pig_p		0			3			0		 709	516	881	682
# ----------------------------------------------------------------------------
#
# @author	: GyeongBong Kim
# @Date		: Tue, 3 Mar, 2020 
Revision:
	- 20 Apr, 2020 Support arguments to merge into jetson nano training tool-chain by K.M.Jeon
"""

import pandas as pd
import os
from io import open
import argparse


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--data_path', help='input data path where label and meta folders are located',
						default='.')
	args = parser.parse_args()
	

	HOME = args.data_path

	train_label = pd.read_csv(HOME+'/retinanet_type_annotation.csv', sep=',', header=None)
	#val_label = pd.read_csv(HOME+'/retinanet_type_annotation.csv', sep=',', header=None)
	mapping_info = pd.read_csv(HOME+'/retinanet_type_class_mapping.csv', sep=',', header=None)


	"""
	1. For train label
	We create 3D object detection format.
	"""
	## 1.train list
	# File_Path, x1, y1, x2, y2, class

	for index, rows in train_label.iterrows():
		file_name_tmp = rows[0]
		file_name = os.path.splitext(os.path.split(file_name_tmp)[-1])[0]

		x_min = rows[1]
		y_min = rows[2]
		x_max = rows[3]
		y_max = rows[4]
		class_type = rows[5] 

		label_folder_path = os.path.join(HOME, 'lab_kitti_train')
		if not os.path.exists(label_folder_path):
			os.mkdir(label_folder_path)

		with open(os.path.join(label_folder_path, file_name+'.txt'), 'a') as txt_file:
			img_info = [class_type, 0.0, 0, 0.0, x_min, y_min, x_max, y_max, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # class_type, truncated, occluded, alpha, bbox
			write_path = " ".join(map(str, img_info)) + '\n'
			txt_file.write(write_path.decode('utf-8'))
			# txt_file.write('\n')

	
	#if not (val_label == train_label):
	#	"""
	#	2. For valid label
	#	We create 3D object detection format.
	#	"""
	#	## 1.valid list
	#	# File_Path, x1, y1, x2, y2, class
    #
	#	for index, rows in val_label.iterrows():
	#		file_name_tmp = rows[0]
	#		file_name = os.path.splitext(os.path.split(file_name_tmp)[-1])[0]
    #
	#		x_min = rows[1]
	#		y_min = rows[2]
	#		x_max = rows[3]
	#		y_max = rows[4]
	#		class_type = rows[5] 
	#		# train_label_list.append([rows[0], rows[1], rows[2], rows[3], rows[4], rows[5]])
    #
	#		label_folder_path = os.path.join(HOME, 'lab_kitti_val')
	#		if not os.path.exists(label_folder_path):
	#			os.mkdir(label_folder_path)
    #
	#		with open(os.path.join(label_folder_path, file_name+'.txt'), 'a') as txt_file:
	#			img_info = [class_type, 0.0, 0, 0.0, x_min, y_min, x_max, y_max, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # class_type, truncated, occluded, alpha, bbox
	#			write_path = " ".join(map(str, img_info)) + '\n'
	#			txt_file.write(write_path.decode('utf-8'))
	#			# txt_file.write('\n')
			

if __name__ == '__main__':
	main()		