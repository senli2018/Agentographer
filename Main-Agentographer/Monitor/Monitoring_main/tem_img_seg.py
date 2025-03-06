def ocr_crop():
    from PIL import Image
    image_path = r'D:\work\AgentAI_ls_309\模板图片\调整定位片范围界面.jpg'
    with Image.open(image_path) as img:
        # 定义裁剪区域（左上角）
        left  = 960  +  960 - 438
        top   = 1000 -  80
        right = 960  +  960
        bottom= 990  +  52
        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        output_image_path = r'D:\work\AgentAI_ls_309\模板图片裁剪后\X光片界面-正片扫描界面.jpg'
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
def ocr_crop_input_inbed_screen(image_path):
    from PIL import Image
    # image_path = r'D:\work\AgentAI_ls_309\模板图片\调整定位片范围界面.jpg'
    with Image.open(image_path) as img:
        # 定义裁剪区域（左上角）
        left  = 960  +  960 - 438
        top   = 1000 -  80
        right = 960  +  960
        bottom= 990  +  52
        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        output_image_path = r'after_seg\temp_seg\2_temp.jpg'
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
        return output_image_path

def ocr_crop_scout(image_path):
    from PIL import Image

    with Image.open(image_path) as img:
        # 定义裁剪区域（左上角）
        left = 960 + 960 - 438
        top = 1000 - 80
        right = 960 + 960
        bottom = 990 + 52
        # 裁剪图像
        cropped_img = img.crop((left, top, right, bottom))
        output_image_path = r'after_seg\temp_seg\3_temp.jpg'
        # 保存裁剪后的图像
        cropped_img.save(output_image_path)
        return output_image_path

if __name__ == '__main__':
    pass
##患者信息界面
#不需要新的

## 定位片扫描的区域
# left = 960 + 960 - 438
# top = 1000 - 80
# right = 960 + 960
# bottom = 990 + 52

## 输入进床深度区域
# left = 960 + 960 - 438
# top = 1000 - 80
# right = 960 + 960
# bottom = 990 + 52

## 调整定位片范围界面
# left = 960 + 960 - 438 + 30
# top = 1000 - 80 - 200 - 50 - 50 + 30
# right = 960 + 960 - 200
# bottom = 990 - 200 - 50 - 50

## 正片扫描界面
# left = 960 + 960 - 438 - 17 + 10 + 5 + 5
# top = 1000 - 80 + 20 + 20 + 30
# right = 960 + 960 - 20 - 30 - 240
# bottom = 990 + 20 + 10 + 10 + 10

## 退床界面






