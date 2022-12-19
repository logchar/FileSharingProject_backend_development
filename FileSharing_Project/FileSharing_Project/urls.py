"""FileSharing_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.staticfiles import views as my_view

from FileSharing_Project.log_reg import log_reg
from Files.views import *
from Users.views import *

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', my_view.serve),  # 头像图片存储
    path("admin/", admin.site.urls),
    path("login/", log_reg),  # 登录

    path("users/<int:pk>", UserViewSet.as_view({'get': 'get_userinfo'})),
    path("users/<int:pk>", UserViewSet.as_view({'post': 'get_userfile_list'})),
    path("users/<int:pk>", UserViewSet.as_view({'put': 'perform_update_userinfo'})),

    path("files/", FileViewSet.as_view({'get': 'get_list'})),
    path("files/", FileViewSet.as_view({'post': 'perform_upload'})),
    path("files/<int:pk>/", FileViewSet.as_view({'get': 'get_detail'})),
    path("files/<int:pk>/", FileViewSet.as_view({'put': 'perform_change'})),
    path("files/<int:pk>/", FileViewSet.as_view({'delete': 'perform_delete'})),

    path("collections/<int:pk>", CollectionView.as_view()),

    path("downloads/<int:pk>", DownloadView.as_view()),

    path("search/", FileViewSet.as_view({'get': 'perform_search'})),
]
