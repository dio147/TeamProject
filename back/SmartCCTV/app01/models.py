from pyexpat import model
from time import sleep
from django.db import models


# Create your models here.
class teacher_account(models.Model):
    """this is teacher account model"""
    tid = models.CharField('教师编号', primary_key=True, max_length=50)
    taccount = models.CharField('教师用户名', null=False, max_length=50)
    tpassword = models.CharField('教师密码', null=False, max_length=50)

    class Meta:
        db_table = 'teacher_account'
        verbose_name = "教师管理"
        verbose_name_plural = verbose_name


class teacher_info(models.Model):
    """this is teacher information model"""
    tid = models.OneToOneField(teacher_account, primary_key=True, on_delete=models.CASCADE)
    tname = models.CharField("教师姓名", null=False, max_length=50)
    tsex = models.BooleanField("教师性别", default=True, null=False)
    tschool = models.CharField("教师学校", null=False, max_length=50)

    class Meta:
        db_table = "teacher_infomation"
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name


class ALLCCTV(models.Model):
    cctv = models.CharField('cctv', primary_key=True, max_length=50)
    update_num = models.IntegerField("update_num", null=True)

    class Meta:
        db_table = "all_cctv"
        verbose_name = "cctv"
        verbose_name_plural = verbose_name


class class_info(models.Model):
    cid = models.CharField("班级编号", primary_key=True, max_length=50)
    grade = models.IntegerField("年级", null=False)
    cnumber = models.IntegerField("班级号", null=False)
    cctv = models.OneToOneField(ALLCCTV, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "class_information"
        verbose_name = "班级信息"
        verbose_name_plural = verbose_name


class teacher_class(models.Model):
    cid = models.OneToOneField(class_info, primary_key=True, on_delete=models.CASCADE)
    tid = models.ForeignKey(teacher_account, on_delete=models.CASCADE)

    class Meta:
        db_table = "teacher_class"
        verbose_name = "教师类"
        verbose_name_plural = verbose_name


class student_info(models.Model):
    sid = models.CharField("学生编号", primary_key=True, max_length=50)
    sname = models.CharField("学生姓名", null=False, max_length=50)
    spic = models.CharField("学生照片", null=False, max_length=100)
    cid = models.ForeignKey(class_info, on_delete=models.CASCADE)

    class Meta:
        db_table = "student_infomation"
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name


class student_daily_data(models.Model):
    date = models.DateField("数据日期", null=False)
    sid = models.ForeignKey(student_info, on_delete=models.CASCADE)
    totle_time = models.FloatField("总时长", null=False)
    up_time = models.FloatField("抬头时长", null=False)
    down_time = models.FloatField("低头时长", null=False)
    sleep_time = models.FloatField("趴下时长", null=False)

    class Meta:
        db_table = "student_daily_data"
        unique_together = ("date", "sid")
        verbose_name = "数据"
        verbose_name_plural = verbose_name
