import requests
from ct_group.config.device_cfg import ct_seg_ip,deep_camera_ip
def ct_seg_request(data):
    url = "http://{}/mask/intact/".format(ct_seg_ip)
    pic_path = 'D:\AgentAI_ls\iner_pic\ct_seg_raw.jpg'
    # pic_path1 = 'D:\AgentAI_ls\iner_pic\ct_seg_raw.jpg'
    data.save(pic_path)
    # 这里用的open打开的图像数据
    # files = {'image': open('D:\\work\\ct_agent001\\ct_agent_001\\get_video\\psudo_img\\举手（side）_proc.jpg', 'rb')}
    files = {'image': open(pic_path, 'rb')}
    # files = {'image': data.tobytes()}

    # 注意：headers 参数在这里是不需要的，因为 requests 会自动设置正确的 content-type
    response = requests.post(url, files=files)

    # 确保文件被正确关闭
    files['image'].close()
    print(response.text)
    return response.text

def deep_camera():
    import json
    # url = "http://{}/pose_right_or_wrong/".format(position_request_ip)
    url = "http://{}/neck/plane/depth".format(deep_camera_ip)
    # 注意：headers 参数在这里是不需要的，因为 requests 会自动设置正确的 content-type
    response = requests.get(url) # 12.19解开注释 没使用timeout 因为今天的移床时间返回很慢
    result = json.loads(response.text)
    point_distance=result["point_distance"]  # 补充point_distance注释
    print(point_distance)
    # in_bed_distance= 0.0066*point_distance**2-1.9749*point_distance-170.6936
    xiong_hou=result["xiong_hou"]
    #print(point_distance)
    print(xiong_hou)
    end_point=result["end_point"]
    #print(point_distance)
    print(end_point)
    return point_distance,xiong_hou,end_point

def append_to_txt_file(point_distance, xiong_hou, filename):
    from datetime import datetime
    # 拼接要写入文件的字符串
    current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_str = f"time: {current_time},ID: {point_distance}, xiong_hou: {xiong_hou}\n"

    # 将拼接好的字符串追加到文件
    with open(filename, "a") as f:
        f.write(data_str)

if __name__ == "__main__":
    deep_camera()


