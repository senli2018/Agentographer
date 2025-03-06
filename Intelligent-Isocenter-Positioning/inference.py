# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser

from mmcv.image import imread

from mmpose.apis import inference_topdown, init_model
from mmpose.registry import VISUALIZERS
from mmpose.structures import merge_data_samples
import cv2
import copy
import math
import os
import ast
from argparse import ArgumentParser

from mmengine.logging import print_log

from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes
import numpy as np
import cv2

# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser

from mmengine.fileio import dump
from rich import print_json

from mmpretrain.apis import ImageClassificationInferencer

def distance_point_to_line(x0, y0, x1, y1, x2, y2):
    # 计算向量 P1P2 和 P0P1
    P1P2 = (x2 - x1, y2 - y1)
    P0P1 = (x1 - x0, y1 - y0)
    
    # 计算叉积的模长，即点到直线的距离
    cross_product = P1P2[0] * P0P1[1] - P1P2[1] * P0P1[0]
    distance = abs(cross_product) / math.sqrt(P1P2[0]**2 + P1P2[1]**2)
    
    return distance

def crop_image_point_restore(left_top_coord,right_bottom_coord,result_point):
    left = left_top_coord[0]
    right = right_bottom_coord[0]
    top = left_top_coord[1]
    down = right_bottom_coord[1]
    new_result_point = result_point + np.array([left, top])
    return new_result_point.astype(np.uint16)

def above_img_inference(ori_img_data, out_path: str = 'infer_result.png'):
    # TODO 将图像进行裁剪
    #image裁剪
    left_top_coord = [380, 310]
    right_bottom_coord = [1608,706]

    crop_img_data = ori_img_data[left_top_coord[1]:right_bottom_coord[1], left_top_coord[0]:right_bottom_coord[0]]
    # crop_img_data = cv2.rotate(crop_img_data,cv2.ROTATE_90_COUNTERCLOCKWISE)
    crop_rotate_img_path = './crop_rotate_img.jpg'
    cv2.imwrite(crop_rotate_img_path, crop_img_data)
    
    # build the model from a config file and a checkpoint file
    cfg_options = None
    config_path = "/www/wwwroot/get_and_above/imageprocessor/human_detection/DWPose/mmpose/configs/wholebody_2d_keypoint/rtmpose/ubody/rtmpose-l_8xb32-270e_coco-ubody-wholebody-384x288.py"
    ckpt_path = "/www/wwwroot/get_and_above/imageprocessor/human_detection/DWPose/mmpose/dw-ll_ucoco_384.pth"
    model = init_model(config_path, ckpt_path, device="cuda:0", cfg_options=cfg_options)

    # init visualizer
    model.cfg.visualizer.radius = 3
    model.cfg.visualizer.alpha = 0.8
    model.cfg.visualizer.line_width = 1

    visualizer = VISUALIZERS.build(model.cfg.visualizer)
    visualizer.set_dataset_meta(model.dataset_meta, skeleton_style='mmpose')

    # inference a single image
    batch_results = inference_topdown(model, crop_rotate_img_path)
    results = merge_data_samples(batch_results)

    keypoints_dict = {}
    # 获取关键点的结果
    keypoints = results.pred_instances['keypoints']
    new_keypoints = keypoints[0]
    for i,point in enumerate(new_keypoints):
        new_keypoints[i] = crop_image_point_restore(left_top_coord, right_bottom_coord, point)
    
    shoulder = cal_center_point(new_keypoints[5],new_keypoints[6])
    hip = cal_center_point(new_keypoints[11],new_keypoints[12])
    knee = cal_center_point(new_keypoints[13],new_keypoints[14])
    C1 = new_keypoints[54]
    C5 = new_keypoints[31]
    C7 = shoulder
    L5 = hip # 位置下挪，直接使用hip
    T11 = cal_center_point(shoulder,hip)
    T11 = cal_center_point(shoulder,T11) # 向上挪
    L3 = cal_center_point(hip,T11) # hip和新T11中点
    hip = cal_center_point(hip,knee) # hip往下挪，重新定位 取hip与膝中点

    #返回所有关键点坐标的字典
    keypoints_dict = {
        # "shoulder": shoulder.tolist(), # 用C7代替显示
        "hip": hip.tolist(),
        "knee": knee.tolist(),
        "C1": C1.tolist(),
        "C5": C5.tolist(),
        "C7": C7.tolist(),
        "L3": L3.tolist(),
        "T11": T11.tolist(),
        "L5": L5.tolist(),
    }

    # 扫描颅脑：0 - C5
    # 扫描胸部：C5 - L3
    # 扫描腹部（腰椎）：T11 - L5
    # 扫描盆部：L3 - Hip

    return keypoints_dict
def cal_center_point(point1, point2):
    """计算两个点的中点"""
    midpoint = (point1 + point2) / 2
    return midpoint

def cal_dis(point1, point2):
    """计算两个点之间的欧氏距离"""
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def get_bed_center_line(image, src_points):
    """通过透视变换获取床的中心线"""
    target_width, target_height = 240, 688
    dst_points = np.array([
        [0, 0], 
        [target_width, 0], 
        [0, target_height], 
        [target_width, target_height]
    ], dtype=np.float32)
    
    # 计算透视变换矩阵并进行透视变换
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped_img = cv2.warpPerspective(image, matrix, (target_width, target_height))
    
     # 使用透视变换后的图像角点计算中线
    top_midpoint = cal_center_point(dst_points[0], dst_points[1])  # 上边中点
    bottom_midpoint = cal_center_point(dst_points[2], dst_points[3])  # 下边中点
    
    return warped_img, top_midpoint, bottom_midpoint


def draw_keypoints_with_labels(image, keypoints, labels, midline_start, midline_end):
    """
    绘制关键点和中线到图像上，同时在点附近显示标签
    :param image: 待绘制的图像
    :param keypoints: 关键点坐标列表 [(x1, y1), (x2, y2), ...]
    :param labels: 对应关键点的标签 ["label1", "label2", ...]
    :param midline_start: 中线起点坐标 (x, y)
    :param midline_end: 中线终点坐标 (x, y)
    :return: 带绘制的图像
    """
    img_copy = image.copy()
    
    # 绘制中线
    cv2.line(img_copy, midline_start, midline_end, (0, 255, 0), 2)
    
    # 绘制关键点和标签
    for point, label in zip(keypoints, labels):
        x, y = int(point[0]), int(point[1])
        cv2.circle(img_copy, (x, y), 5, (0, 0, 255), -1)  # 绘制关键点
        cv2.putText(img_copy, label, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)  # 绘制标签
    
    return img_copy


def calculate_distances_to_top(keypoints, labels, pixel_to_cm=0.25):
    """
    计算各关键点到图像顶端边线的垂直距离，并转换为厘米
    :param keypoints: 关键点坐标列表 [(x1, y1), (x2, y2), ...]
    :param labels: 对应关键点的标签 ["label1", "label2", ...]
    :param pixel_to_cm: 像素到厘米的转换比例，默认1像素=0.25cm
    :return: 字典，包含每个关键点到顶端边线的垂直距离（单位：厘米）
    """
    distances_to_top = {}
    
    for label, point in zip(labels, keypoints):
        # 计算点到顶端边线的垂直距离
        vertical_distance = point[1]  # y坐标即为到顶端的距离
        # 转换为厘米
        distance_in_cm = vertical_distance * pixel_to_cm
        distances_to_top[label] = distance_in_cm
    
    return distances_to_top

# def test_keypoints_on_image(image_path):
def test_keypoints_on_image(input_dir, file_name):
    """测试单张图像的关键点检测、透视变换、距离计算和绘图"""
    image_path = os.path.join(input_dir, file_name)
    print(f"Reading image from: {image_path}")

    ori_img_data = cv2.imread(image_path)
    # ori_img_data = image_path
    # 检查图像是否成功读取
    if ori_img_data is None:
        raise FileNotFoundError(f"Failed to load image at: {image_path}. Please check the file path and ensure the file exists.")

    output_dir = "/home/senlee/data1/joe/Guoaoshuai/bushu_test/iner_pic_results/"

    # 床的四个角点（根据透视变换的实际需要调整坐标）
    src_points = np.array([
        (520, 156), (708, 156), (501, 719), (698, 719)
    ], dtype=np.float32)

    # 获取透视矫正后的图像和中线
    warped_img, top_midpoint, bottom_midpoint = get_bed_center_line(ori_img_data, src_points)
    
    # 使用变换后的图像进行关键点检测
    keypoints_dict, crop_image = test_above_img_inference(warped_img)
    
    # 提取关键点
    keypoints = [
        tuple(keypoints_dict["C1"]),
        tuple(keypoints_dict["C5"]),
        tuple(keypoints_dict["C7"]),
        tuple(keypoints_dict["L3"]),
        tuple(keypoints_dict["T11"]),
        tuple(keypoints_dict["L5"]),
        tuple(keypoints_dict["eyebrow"]),
        tuple(keypoints_dict["shoulder_L"]),
        tuple(keypoints_dict["shoulder_R"]),
        tuple(keypoints_dict["hip"]),
        tuple(keypoints_dict["knee"]),
        tuple(keypoints_dict["foot"]),
    ]

    labels = list(keypoints_dict.keys())
    
    # 计算距离
    distances = calculate_distances_to_top(keypoints, labels)  # Point to image top distance  

    # 绘制结果
    midline_start = (int(top_midpoint[0]), int(top_midpoint[1]))
    midline_end = (int(bottom_midpoint[0]), int(bottom_midpoint[1]))
    result_image = draw_keypoints_with_labels(warped_img, keypoints, labels, midline_start, midline_end)

    # 保存透视变换后的图像和最终结果
    base_filename = os.path.basename(image_path)
    filename_without_ext = os.path.splitext(base_filename)[0]

    # 保存结果图片
    result_image_path = os.path.join(output_dir, f"{filename_without_ext}_result.png")
    cv2.imwrite(result_image_path, result_image)
    
    # 保存距离信息
    distance_file_path = os.path.join(output_dir, f"{filename_without_ext}_distances.txt")
    with open(distance_file_path, "w") as f:
        for label, distance in distances.items():
            f.write(f"{label}: {distance:.2f} cm\n")

    return distances


# not use, just for
def process_all_images(input_dir, output_dir):
    """批量处理目录中的所有图像"""
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 遍历目录中的所有图片
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # 检查文件格式
            print(f"Processing: {file_name}")
            distances = test_keypoints_on_image(file_path, output_dir)
            print(f"Distances for {file_name}:")
            print(distances)





########################################################################################################################
if __name__ == '__main__':
    # image = cv2.imread('./vision_image/color_image.jpg')

    # result = above_img_inference(image)
    # print("{}mm".format(result))
    # img_data = cv2.imread('/home/senlee/data1/joe/Guoaoshuai/human_detection/DWPose/psudo_img/test_side/captured_image.jpg')
    # result = side_img_inference(img_data)
    # print("{}s".format(result))


    input_dir = "/home/senlee/data1/joe/Guoaoshuai/bushu_test/iner_pic_use/"
    file_name = "image_test1.jpg"
# 调用函数
    distances = test_keypoints_on_image(input_dir, file_name)
    print(distances)
    # ok 
    # img_path = "/home/senlee/data1/joe/Guoaoshuai/get_and_above/demo_test/1.jpg"
    # img_data = cv2.imread(img_path)
    # result = lie_or_not(img_data)
    # print(result)