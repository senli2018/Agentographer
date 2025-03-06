from .function import common_cam,Big_model_picture,Big_model_video,if_open_door
from django.http import HttpResponse,JsonResponse
import json
def CommonCam_view(request):
    if request.method == 'GET':
        common_cam()
        print("方舱摄像头已经拍摄")
        return HttpResponse("方舱摄像头已经进行拍摄", status=200)
    else:
        # 如果不是POST请求，返回错误
        return HttpResponse("请使用get请求", status=405)


def Bigmodel_picture_view(request):
    if request.method == 'GET':
        data=Big_model_picture()
        json_data = json.dumps(data)  # 将字典转换为JSON格式的字符串
        return HttpResponse(json_data, content_type='application/json')  # 返回JSON字符串
def Bigmodel_video_view(request):
    if request.method == 'GET':
        data=Big_model_video()
        json_data = json.dumps(data)  # 将字典转换为JSON格式的字符串
        return HttpResponse(json_data, content_type='application/json')  # 返回JSON字符串

def Bigmodel_video_door_view(request):
    if request.method == 'GET':
        data=if_open_door()
        json_data = json.dumps(data)  # 将字典转换为JSON格式的字符串
        return HttpResponse(json_data, content_type='application/json')  # 返回JSON字符串