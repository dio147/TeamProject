"""SmartCCTV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # this is a test path
    path('testget/', views.testget),
    path('testpost/', views.testpost),
    path('saveinfo/teacher/', views.save_teacher_info),
    path('saveinfo/createClass/', views.create_class),
    path('login/', views.login),
    path('regist/', views.regist),
    path('initDataP1/', views.init_MainWindowP1),
    path('initStudentData/', views.init_StudentData),
    path('stu_info/save/', views.import_stu_info),
    path('sid_sname/choose/', views.choose_stu_name),
    path('student_picture/post/', views.post_student_picture),
    path('student_daily/post/', views.get_stu_daily_data),
    path('bent/cctv/', views.bent_class_cctv),
    path('class/choose/', views.choose_class),
    path('cctv/choose/', views.choose_cctv),
    path("send/stu_pic/", views.send_stu_pic)
]
