from django.urls import path
from .views import *

urlpatterns =[
    path("getId/", getId, name="getId"),
    path("upload/", upload, name="upload"),
    path("", index, name="home"),
]