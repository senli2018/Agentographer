import time
from CFG_GLOBAL import AGENT_RUN_DIR
import os
import cv2

def calculate_similarity_with_template_new(screen_img, templates):
    """
    对屏幕截取区域与多个模板进行匹配，并返回最高匹配的模板及其分数。
    :param screen_img: 截取的屏幕区域图像
    :param templates: 模板图像列表
    :return: 最相似模板的索引及其匹配分数
    """
    max_similarity = -1
    best_template_idx = -1
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)

    for idx, template in enumerate(templates):
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(f"template {idx} Match score: {max_val}")

        if max_val > max_similarity:
            max_similarity = max_val
            best_template_idx = idx
    return best_template_idx+1, max_similarity
def ocr_inital():
    from ct_group.visionAi.vision_utils import ocr_crop
    print("ocr_inital")
    template2 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/2_after.jpg'))
    template3 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/3_after.jpg'))
    # 模板列表
    img_paths = [template2, template3]
    max_attempts = 20
    attempts = 0
    while attempts < max_attempts:
        # 找到最匹配的图片序号
        ocr_crop()
        target_img_path = cv2.imread(os.path.join(AGENT_RUN_DIR,'bed_right_or_wrong/bed_resize.jpg'))
        result,data =calculate_similarity_with_template_new(target_img_path, img_paths)
        print(f"The best matching picture sequence number is: {result}")

        # 如果匹配值是1，退出循环
        if result == 2:
            print("The match is successful! Exit the loop.")
            break
        else:
            # 打印信息并休眠一秒
            print("The matching value is not 2. Please try again....")
            time.sleep(3)
        # 增加尝试计数
        attempts += 1
        if attempts == max_attempts:
            print("When the maximum number of attempts is reached, exit the loop.")
            break
def ocr_inital_oneclick_to_scan():
    print("ocr_inital_oneclick_to_scan")
    from ct_group.visionAi.vision_utils import ocr_crop

    # template1 = cv2.imread(r'D:\AgentAI_ls\process_picture\1_after.jpg')
    template2 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/2_after.jpg'))
    template3 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/4_after.jpg'))

    # 模板列表
    img_paths = [ template2, template3]
    # target_img_path = r'D:\AgentAI_ls\bed_right_or_wrong\bed_resize.jpg'
    # target_img_path = r'D:\AgentAI_ls\ct_group\patientinfo\3.jpg'

    # img_paths = [r'D:\AgentAI_ls\ct_group\patientinfo\1.jpg', r'D:\AgentAI_ls\ct_group\patientinfo\2.jpg', r'D:\AgentAI_ls\ct_group\patientinfo\4.jpg']
    max_attempts = 20
    attempts = 0

    while attempts < max_attempts:
        # 找到最匹配的图片序号
        ocr_crop()
        target_img_path = cv2.imread(os.path.join(AGENT_RUN_DIR,'bed_right_or_wrong/bed_resize.jpg'))
        # result = find_most_similar(target_img_path, img_paths)
        result, data = calculate_similarity_with_template_new(target_img_path, img_paths)
        print(f"The best matching picture sequence number is. {result}")
        # 如果匹配值是1，退出循环
        if result == 2:
            print("The match is successful! Exit the loop.")
            break
        else:
            # 打印信息并休眠一秒
            print("The matching value is not 2. Please try again...")
            time.sleep(2.5)
        # 增加尝试计数
        attempts += 1
        if attempts == max_attempts:
            print("When the maximum number of attempts is reached, exit the loop.")
def ocr_scan_complete():
    print("ocr_scan_complete")
    from ct_group.visionAi.vision_utils import ocr_crop

    template1 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/4_after.jpg'))
    template2 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/5_after.jpg'))
    template3 = cv2.imread(os.path.join(AGENT_RUN_DIR,'process_picture/6_after.jpg'))
    img_paths = [template1, template2, template3]
    # target_img_path = r'D:\AgentAI_ls\bed_right_or_wrong\bed_resize.jpg'
    # target_img_path = r'D:\AgentAI_ls\bed_right_or_wrong\6.jpg'

    # img_paths = [r'D:\AgentAI_ls\ct_group\patientinfo\4.jpg', r'D:\AgentAI_ls\ct_group\patientinfo\5.jpg', r'D:\AgentAI_ls\ct_group\patientinfo\6.jpg']
    max_attempts = 20
    attempts = 0

    while attempts < max_attempts:
        # 找到最匹配的图片序号
        ocr_crop()
        target_img_path = cv2.imread(r'D:\Monitoring_AI\bed_right_or_wrong\bed_resize.jpg')
        # result = find_most_similar(target_img_path, img_paths)
        result, data = calculate_similarity_with_template_new(target_img_path, img_paths)
        print(f"The best matching picture sequence number is: {result}")
        # 如果匹配值是1，退出循环
        if result == 3:
            print("The match is successful! Exit the loop.")
            break
        else:
            # 打印信息并休眠一秒
            print("The matching value is not 3. Please try again...")
            time.sleep(1)
        # 增加尝试计数
        attempts += 1
    if attempts == max_attempts:
        print("When the maximum number of attempts is reached, exit the loop.")









if __name__ == "__main__":
    pass
