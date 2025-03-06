# import sys
# sys.path.append("./lung_segmentation")
import os
os.chdir("lung_segmentation")
import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from sam2.build_sam import build_sam2_video_predictor
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pydicom
import time
import json
import time
import random
import uvicorn
import requests
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

model = dict()

class Item(BaseModel):
    image: UploadFile

def get_point_list(points_1, points_0):
    new_point_list = points_1 + points_0
    random.shuffle(new_point_list)
    label_list = []
    for i in new_point_list:
        if i in points_1:
            label_list.append(1)
        else:
            label_list.append(0)
    input_point = np.array(new_point_list)
    input_label = np.array(label_list)
    return input_point, input_label

def get_lung_positon(img_path):
    save_name = os.path.basename(img_path).split('.')[0]
    start_time = time.time()
    predictor = model["sam2"]
    points_1, points_0, image, left, right = preprocess_image(img_path)
    cv2.imwrite(f"./vision_result/{save_name}_resize.jpg", image)
    input_point, input_label = get_point_list(points_1, points_0)
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
        predictor.set_image(image)
        masks, scores, _ = predictor.predict( 
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )
    masks = masks[0:1]
    cv2.imwrite("./vision_result/mask.jpg",masks[0]*255)

    masks = (masks[0] * 255).astype(np.uint8)

    contours, _ = cv2.findContours(masks, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    new_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            new_contours.append(contour)
    new_mask = np.zeros_like(masks)
    if new_contours is not None:
        cv2.drawContours(new_mask, new_contours, -1, 255, -1)


    image[new_mask == 255] = [0, 255, 0]    
    top_pos = np.min(np.where(new_mask == 255)[0])
    bottom_pos = np.max(np.where(new_mask == 255)[0]) 
    image[top_pos:top_pos+1]=[0,0,255]
    image[bottom_pos:bottom_pos+1]=[0,0,255]
    image[:, left:left+1]=[0,0,255]
    image[:, right:right+1]=[0,0,255]
    cv2.imwrite(f"./vision_result/{save_name}_box.jpg",image)
    print(time.time()-start_time)
    return top_pos, bottom_pos, left, right


def preprocess_image(image_path):
    save_name = os.path.basename(image_path).split('.')[0]
    image = cv2.imread(image_path)
    image = cv2.resize(image, (960, 1080))
    image_resize = np.copy(image)
    os.makedirs("./vision_result",exist_ok=True)
    # cv2.imwrite("./vision_result/resize.jpg", image)

    new_mask = np.zeros_like(image)
    new_mask[220:860,7:372] = image[220:860,7:372]
    image = new_mask

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = gray.astype(np.uint8)
    mean = np.mean(gray)
    # gray[gray < mean] = 0

    # print("image mean:",mean)

    ret,threshold = cv2.threshold(gray,mean,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    kernel = np.ones((3,3),np.uint8)
    threshold = cv2.erode(threshold, kernel, iterations=2)  

    cv2.imwrite("./vision_result/{}_threshold.jpg".format(save_name), threshold)

    # 找到二值图像中的所有连通域
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化一个变量来保存最大面积的连通域
    max_area = 0
    max_contour = None

    # 遍历所有连通域并找到面积最大的连通域
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    mask = np.zeros_like(threshold)
    if max_contour is not None:
        cv2.drawContours(mask, [max_contour], -1, 255, -1)

    non_zero_pixels = cv2.findNonZero(threshold)
    if non_zero_pixels is not None:
        # 提取所有非零像素的x和y坐标
        x_coords = non_zero_pixels[:, :, 0]
        y_coords = non_zero_pixels[:, :, 1]
        
        # 计算x和y坐标的平均值
        centroid_x = int(np.mean(x_coords))
        centroid_y = int(np.mean(y_coords))

        # 人体估计质心
        point_center = (centroid_x, centroid_y)

        #质心点所在的长宽，（腰宽和身长）
        distance_y = sum(threshold[:,centroid_x]==255)
        distance_x = sum(threshold[centroid_y,:]==255)

        item_dis_y = distance_y/16
        item_dis_x = distance_x/16

        # 正向坐标点
        point_pos = [
            [int(centroid_x+item_dis_x*(-3)), int(centroid_y+item_dis_y*(-3))],
            [int(centroid_x+item_dis_x*(3)), int(centroid_y+item_dis_y*(-4))],
            [int(centroid_x+item_dis_x*(-4)), int(centroid_y+item_dis_y*(-1))],
            [int(centroid_x+item_dis_x*(4.5)), int(centroid_y+item_dis_y*(1))],

        ]

        # 反向坐标点
        point_neg = [
            [int(centroid_x+item_dis_x*(-4)), int(centroid_y+item_dis_y*(5))],
            [int(centroid_x+item_dis_x*(4)), int(centroid_y+item_dis_y*(5))],
            [int(centroid_x+item_dis_x*(-4)), int(centroid_y+item_dis_y*(-7))],
            [int(centroid_x+item_dis_x*(4)), int(centroid_y+item_dis_y*(-7))],

        ]

        # image = draw_points(point_center, image)

        for point in point_pos:
            image = draw_points(point, image, color=255)


        for point in point_neg:
            image = draw_points(point, image, color=0)

    left = centroid_x - int(distance_x / 2)
    right = centroid_x + int(distance_x /2)

    cv2.imwrite("./vision_result/{}_image.jpg".format(save_name), image)
    return point_pos, point_neg, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), left, right

@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpoint = "./checkpoints/sam2_hiera_large.pt"
    model_cfg = "sam2_hiera_l.yaml"
    model["sam2"]  = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint))
    yield
    model.clear()

def draw_points(point, mask, color=0):
    for i in range(-5,5):
        for j in range(-5,5):
            mask[point[1]+i, point[0]+j] = color
    return mask

app = FastAPI(lifespan=lifespan)

@app.post('/mask/intact/')
def mask_interactivate(image: UploadFile=File(None)):
    file = image
    try:
        if file is None:
            image_path = "2.jpg"
        else:
            filename = f"{time.time()}_{file.filename}"
            image_path = os.path.join(os.getcwd(), "origin_images",filename)
            image_bytes = file.file.read()
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

        print("image_path1:", image_path)
        # 假设get_lung_positon是你定义的一个函数
        top_pos, bottom_pos, left_pos, right_pos = get_lung_positon(image_path)
        print("now: top_pos:", top_pos, "bottom_pos:", bottom_pos)
        print("now: left_pos:", left_pos, "right_pos:", right_pos)

        data = {
            'top_pos': float(top_pos),
            'bottom_pos': float(bottom_pos),
            'left_pos': float(left_pos),
            'right_pos': float(right_pos)
        }

        return data
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # test 
    checkpoint = "./checkpoints/sam2_hiera_large.pt"
    model_cfg = "sam2_hiera_l.yaml"
    model["sam2"]  = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint))
    test_file_list = os.listdir("./origin_images")
    for file in test_file_list:
        get_lung_positon("./origin_images/"+file)

    
    # inference
    # uvicorn.run(app, host='0.0.0.0', port=7099, log_level="info")
