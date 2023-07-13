# SmartCCTV
实训项目
# 后端(/back)
需要根据情况修改settings.py中的mysql用户密码等配置
配置好环境后需要cd到/back/SmartCCTV路径后在终端输入 python manage.py runserver
后端运行成功后进入http://127.0.0.1:8000/admin/    即可进入django管理页面

# 前端(/front)
运行ProgramMain.py文件即可，如果需要查看不同界面，只需查看Ui_login.py,Ui_main.py即可

# 监控端
可以运行get_face_data.py获取自己的人脸数据，然后运行face2feature.py得到人脸特征
如果想单独运行识别模块可以运行face_reco_from_camera.py查看识别结果

