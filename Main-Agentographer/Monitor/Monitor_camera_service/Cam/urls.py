from . import views
from django.urls import path

urlpatterns = [
    path("commom/", views.CommonCam_view, name="CommonCam_view"),
    path("gptpicture/", views.Bigmodel_picture_view, name="Bigmodel_picture_view"),
    path("gptvideo/", views.Bigmodel_video_view, name="Bigmodel_video_view"),
    path("gptdoor/", views.Bigmodel_video_door_view, name="Bigmodel_video_door_view"),
]


