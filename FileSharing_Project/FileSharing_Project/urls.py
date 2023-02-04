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
    re_path(r'^static/(?P<path>.*)$', my_view.serve),
    path("admin/", admin.site.urls),

    path("login/", log_reg),
    path("collections/<int:pk>/", CollectionView.as_view()),
    path("downloads/<int:pk>/", DownloadView.as_view()),

    path("users/<int:pk>/", UserViewSet.as_view({
        'get': 'get_other_userinfo',
        'post': 'perform_update_avatar'
    })),
    path("user/", UserViewSet.as_view({
        'get': 'get_userinfo',
        'post': 'get_userfile_list',
        'put': 'perform_update_userinfo'
    })),

    path("filelist/<int:pk>/", FileViewSet.as_view({'get': 'get_list'})),
    path("search/", FileViewSet.as_view({'post': 'perform_search'})),
    path("files/<int:pk>/", FileViewSet.as_view({
        'get': 'get_detail',
        'post': 'perform_upload',
        'put': 'perform_change',
        'delete': 'perform_delete'
    })),
]
