import cv2
import os
import numpy as np
import open3d as o3d
import pykinect_azure as pykinect
from pykinect_azure import k4a_float2_t

import numpy as np




def fit_plane_least_squares(points):
    """
    使用最小二乘法拟合平面
    :param points: Nx3 数组，包含N个3D点的坐标
    :return: 平面方程的系数 [a, b, c, d]，对应于 ax + by + cz + d = 0
    """
    # 确保points是一个numpy数组
    points = np.asarray(points)

    # 计算质心
    centroid = np.mean(points, axis=0)

    # 将点集中心化
    centered_points = points - centroid

    # 计算协方差矩阵
    cov = np.cov(centered_points.T)

    # 计算特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    # 找到最小特征值对应的特征向量
    normal = eigenvectors[:, np.argmin(eigenvalues)]

    # 确保法向量指向 "上" 方向
    if normal[2] < 0:
        normal = -normal

    # 计算 d
    d = -np.dot(normal, centroid)

    # 返回平面方程系数 [a, b, c, d]
    return np.append(normal, d)

def calculate_average_distance_to_plane(points, plane_model):
	"""
    计算点云到平面的平均距离
                                       
    :param points: Nx3 数组，包含N个3D点的坐标
    :param plane_model: 平面方程的系数 [a, b, c, d]，对应于 ax + by + cz + d = 0
    :return: 平均距离
    """
	# 确保points是numpy数组
	points = np.asarray(points)

	# 提取平面方程系数
	a, b, c, d = plane_model

	# 计算每个点到平面的距离
	# 距离公式：|ax + by + cz + d| / sqrt(a^2 + b^2 + c^2)
	numerator = np.abs(np.dot(points, [a, b, c]) + d)
	denominator = np.sqrt(a ** 2 + b ** 2 + c ** 2)
	distances = numerator / denominator

	# 计算平均距离
	average_distance = np.mean(distances)

	return average_distance


def get_points_from_url(image):
	import requests
	import json
	url = 'http://192.168.1.195:7861/above/'
	pic_path = './origin_image.jpg'
	cv2.imwrite(pic_path, image)
	files = {'image':open(pic_path,'rb')}
	response = requests.post(url, files=files)
	# print(dict(response.text))
	item = json.loads(response.text) 
	print(item['result'])

	return item['result']	


def get_2d_to_3d_coordinate(pix_coord, transformed_depth_image, device):
    
	pix_x = int(pix_coord[0])
	pix_y = int(pix_coord[1])
	rgb_depth = transformed_depth_image[pix_y, pix_x]

	pixels = k4a_float2_t((pix_x, pix_y))

	# pos3d_color = device.calibration.convert_2d_to_3d(pixels, rgb_depth, pykinect.K4A_CALIBRATION_TYPE_COLOR, pykinect.K4A_CALIBRATION_TYPE_COLOR)
	pos3d_depth = device.calibration.convert_2d_to_3d(pixels, rgb_depth, pykinect.K4A_CALIBRATION_TYPE_COLOR, pykinect.K4A_CALIBRATION_TYPE_DEPTH)
	# print(f"RGB depth: {rgb_depth}, RGB pos3D: {pos3d_color}, Depth pos3D: {pos3d_depth}")
	pos3d_coord = np.array([pos3d_depth.xyz.x, pos3d_depth.xyz.y, pos3d_depth.xyz.z])
	return pos3d_coord


def point_to_plane_distance(point, pix_p1,pix_p2,pix_p3,transformed_depth_image, device):
    # 3 Points on the plane
	# pix_p1_3d = get_2d_to_3d_coordinate(pix_p1, transformed_depth_image, device)
	# pix_p2_3d = get_2d_to_3d_coordinate(pix_p2, transformed_depth_image, device)
	# pix_p3_3d = get_2d_to_3d_coordinate(pix_p3, transformed_depth_image, device)
	# print("p1_3d:{}, p2_3d:{}, p3_3d:{}".format(pix_p1_3d,pix_p2_3d,pix_p3_3d))
	pix_p1_3d = np.array([-524.11730957,-966.58111572, 1457.24707031])
	pix_p2_3d = np.array([75.92230988, -1106.64086914,  1767.79785156])
	pix_p3_3d = np.array([ 752.72619629, -994.40472412, 1511.93115234])
	# pix_point_3d = get_2d_to_3d_coordinate(point, transformed_depth_image, device)
	pix_point_3d = point # the point is neck coord in 3d
	
    # Plane equation
	plane_normal = np.cross(pix_p2_3d - pix_p1_3d, pix_p3_3d - pix_p1_3d)
	plane_normal = plane_normal / np.linalg.norm(plane_normal)
	plane_d = -np.dot(plane_normal, pix_p1_3d)

	# Distance
	distance = np.abs(np.dot(plane_normal, pix_point_3d) + plane_d) / np.linalg.norm(plane_normal)
	
	# # 计算平面上的两个向量
	# vec1 = pix_p2_3d - pix_p1_3d
	# vec2 = pix_p3_3d - pix_p1_3d

    # # 计算平面的法向量（叉积）
	# normal_vector = np.cross(vec1, vec2)

    # # 形成平面方程：ax + by + cz + d = 0
    # # 其中 (a, b, c) 是法向量，(x, y, z) 是平面上的点
	# # a, b, c = normal_vector
	# d = -np.dot(normal_vector, pix_p1_3d)

    # # 计算点4到平面的距离
	# new_distance = np.abs(np.dot(normal_vector, pix_point_3d) + d) / np.linalg.norm(normal_vector)
 
 
	return distance


import time
from flask import Flask, jsonify

plane_param_ok = False
plane_compute_iter = 0
plane_compute_nums_thr = 5

app = Flask(__name__)

@app.route('/neck/plane/depth')
def neck_plane_depth():
	# Initialize the library, if the library is not found, add the library path as argument
	pykinect.initialize_libraries(track_body=True)

	# Modify camera configuration
	device_config = pykinect.default_configuration
	device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
	device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
	device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
	#print(device_config)

	# Start device
	device = pykinect.start_device(config=device_config)

	# Start body tracker
	bodyTracker = pykinect.start_body_tracker()

	# cv2.namedWindow('Color image with skeleton',cv2.WINDOW_NORMAL)
	# cv2.namedWindow('Transformed Color image with skeleton',cv2.WINDOW_NORMAL)

	global plane_param_ok, plane_compute_iter, plane_compute_nums_thr

	print("body_zzhnedepth")
		# Get capture
	capture = device.update()

	# Get body tracker frame
	body_frame = bodyTracker.update()

	# Get the color image
	ret_color, color_image = capture.get_color_image() # 1080x1920x4
	#cv2.imwrite('color_image.png', color_image)

	# Get the depth image
	ret_depth, depth_image = capture.get_depth_image() # 512x512x1
	#cv2.imwrite('depth_image.png', depth_image)
	# depth_imread = cv2.imread('depth_image.png', cv2.IMREAD_UNCHANGED)
	# compar depth image and depth_imread

	# Get the transformed color image
	ret_transformed_color, transformed_color_image = capture.get_transformed_color_image() # 512x512x4
	ret_transformed_depth_depth, transformed_depth_image = capture.get_transformed_depth_image()

	# Get the point cloud
	ret_point, points = capture.get_pointcloud() # Xx3

	# Get the transformed point cloud
	ret_transformed_point, transformed_points = capture.get_transformed_pointcloud() # Xx3

	if not ret_color or not ret_depth or not ret_point or not ret_transformed_point or not ret_transformed_color:
		print("Failed to get images!")
		return jsonify({
			"point_distance": 0,
			"xiong_hou": 0	
		}), 500
	points_map = points.reshape((transformed_color_image.shape[0], transformed_color_image.shape[1], 3)) # 512x512x3
	transformed_points_map = transformed_points.reshape((color_image.shape[0], color_image.shape[1], 3)) # 1080x1920x3
	
	if not os.path.exists("plane_model.txt") and not plane_param_ok:
		print('plane_model no exist')
		plane_model = [0.0, 0.0, 0.0, 0.0]	
		# crop roi from transformed_points_map, roi was geted from color image
		# get roi
		
		# transformed_points_map = transformed_points_map[200:400, 200:400, :] # 200x200x3
		#depth_roi = transformed_points_map[148:159, 1092:1116, :].reshape(-1, 3)
		depth_roi = transformed_points_map[221:228, 911:936, :].reshape(-1, 3)     #平面的位置  前面是g纵坐标，后面是横坐标
		bed_roi = transformed_points_map[421:444, 887:942, :].reshape(-1, 3)      #获取床面上的点
		bed_plane_model=fit_plane_least_squares(bed_roi)

		bed_height = np.sum(bed_roi) / bed_roi.shape[0]

		# np_depth_roi = np.array(depth_roi)
		# convert roi points to open3d format
		# 如果没有法向量和颜色数据，可以不添加
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(depth_roi) #点云数据		
		# extracted plane with open3d apis.
		# o3d.visualization.draw_geometries([pcd], window_name="Random Point Cloud", width=800, height=600)
		#plane_model, inlierss = pcd.segment_plane(distance_threshold=0.1, ransac_n=5, num_iterations=100)
		plane_model=fit_plane_least_squares(depth_roi)



		# inlierss = np.asarray(inlierss)
		# inlier_cloud = pcd.select_by_index(inlierss)		
		# o3d.visualization.draw_geometries([inlier_cloud], window_name="Random Point Cloud", width=800, height=600)

		# compute distance between point and plane_model
		if sum(plane_model) != 0:
			plane_compute_iter = plane_compute_iter + 1
		
		print("plane_compute_iter:", plane_compute_iter)
		print("plane_model: ", plane_model)


		#if 	plane_compute_iter > plane_compute_nums_thr:
		if 	1:	
			plane_param_ok = True
			# save plane_model and bed_height
			plane_file = open("plane_model.txt", "w")
			for i in plane_model:
				plane_file.write(str(round(i, 5)) + '\n')
			plane_file.close()
			print('bh:',bed_height)
			bed_h = open("bed_height.txt", "w")
			for i in bed_plane_model:
				bed_h.write(str(round(i, 5)) + '\n')
			bed_h.close()

	
	# 直接从文件中读取
	else:
		plane_model = []	
		plane_file = open("plane_model.txt", "r")

		for i in range(4):
			line = float(plane_file.readline().rstrip())
			plane_model.append(line)
			print(line)
			# # line = float(plane_file.readline().rstrip())
			# print(float(plane_file.readline().rstrip()))

		bed_plane_model=[]
		bed_file = open("bed_height.txt", "r")
		for i in range(4):
			line_str = bed_file.readline().rstrip()
			if line_str == "":
				continue
			line = float(line_str)
			bed_plane_model.append(line)
		#bed_height = float(bed_file.readline().rstrip())
		#print("bed_height", bed_height)

		#depth_roi = transformed_points_map[316:1437, 421:141, :].reshape(-1, 3)  	
		#plane_model=fit_plane_least_squares(depth_roi)
		#print("plane_model: ", plane_model)


	#xiong_height = np.sum(xiong_roi) / xiong_roi.shape[0]

	#xiong_hou = abs(xiong_height - bed_height)
	print("xiong_hou: ", xiong_hou)

	#######

	key_point = get_points_from_url(color_image)
	start_point = key_point['C5']
	end_point = key_point['L3']
	
	xiong_roi = key_point['L3'] #胸腔位置
	xiong_hou=calculate_average_distance_to_plane(xiong_roi, bed_plane_model)

	result_image = color_image
	print(result_image.shape)
	#key_point=(1000,700)
	cv2.circle(result_image, (int(start_point[0]), int(start_point[1])), 5, (0, 255, 0), -1)
	cv2.imwrite('result_image.jpg',result_image[...,:3])

	print(transformed_depth_image.shape)
	print(key_point[1],key_point[0])
	depth = transformed_depth_image[int(start_point[1]),int(start_point[0])]

	print("depth", depth)
	####### 
	depth_transformed_neck_3d = [key_point[0], key_point[1], int(depth)]
	
	start_point_3d = transformed_points_map[int(start_point[1]),int(start_point[0]), :].reshape(-1,3)
	end_point_3d = transformed_points_map[int(end_point[1]),int(end_point[0]), :].reshape(-1,3)
	#neck_point_3d = transformed_points_map[492,1000, :].reshape(-1,3)

	start_distance=calculate_average_distance_to_plane(start_point_3d, plane_model)
	end_distance=calculate_average_distance_to_plane(end_point_3d, plane_model)
  
	# 0,1 可能存在顺序混乱
	#distance = abs(plane_model[0]*neck_point_3d[0] + plane_model[1]*neck_point_3d[1] + plane_model[2]*neck_point_3d[2] + plane_model[3]) / np.sqrt(plane_model[0]**2 + plane_model[1]**2 + plane_model[2]**2)
			

	# Draw the skeletons into the color image
	color_skeleton = body_frame.draw_bodies(color_image, pykinect.K4A_CALIBRATION_TYPE_COLOR)
	transformed_color_skeleton = body_frame.draw_bodies(transformed_color_image, pykinect.K4A_CALIBRATION_TYPE_DEPTH)

		# cv2.imshow('Color image with skeleton', color_skeleton)
		# cv2.imshow('Transformed Color image with skeleton', transformed_color_skeleton)
		# Press q key to stop
	# time.sleep(20)
	return jsonify({
		"start_distance": int(start_distance),
		"end_distance": int(end_distance),
		"xiong_hou": xiong_hou
	}), 200
		
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7862)
