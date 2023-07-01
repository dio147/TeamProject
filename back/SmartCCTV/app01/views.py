import datetime
import random
from genericpath import exists
import os
import re
from django.forms import ImageField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from .models import ALLCCTV, class_info, student_daily_data, student_info, teacher_class, teacher_info, \
    teacher_account
import json

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import base64


# Create your views here.
def testget(request):
    with open('somename.jpg', 'rb') as f:
        image_byte = base64.b64encode(f.read())
        image_str = image_byte.decode('ascii')
    return JsonResponse({'file': image_str, 'update': 10001})


def testpost(request):
    if request.method == "POST":
        file = request.FILES['img']
        print(file)
        student = student_info.objects.filter(sid='s20191571')
        path = default_storage.save('Images/somename.jpg', ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        return JsonResponse('成功接收', safe=False)
    return JsonResponse('未成功接收', safe=False)


def save_teacher_info(request):
    """
    返回值:
    0 - 信息创建成功
    1 - 信息修改成功
    2 - 找不到该教师，外键错误
    """
    if request.method == "POST":
        print(request.POST)
        teacher = request.POST
        if teacher['sex'] == '男':
            sex = True
        else:
            sex = False
        tas = teacher_account.objects.filter(tid=teacher['tid'])
        # 存在该教师的信息，则直接对原有信息进行修改
        tis = teacher_info.objects.filter(tid=teacher['tid'])
        if tis.exists():
            tis.update(tname=teacher['name'], tsex=sex, tschool=teacher['school'])
            return JsonResponse(1, safe=False)

        # 不存在教师信息，则创建新的信息
        if tas.exists():
            ta = tas.first()
            teacher_info.objects.create(tid=ta, tname=teacher['name'], tsex=sex, tschool=teacher['school'])
            return JsonResponse(0, safe=False)
        else:
            return JsonResponse(2, safe=False)
    return JsonResponse(-1, safe=False)


def create_class(request):
    """
    返回值:
    0 - 创建成功
    1 - 班级已存在 请勿重复创建
    2 - 未找到教师 请检查教师编号
    """
    print(request.POST)
    thisClass = request.POST
    # 判断教师编号是否存在
    teacher = teacher_account.objects.filter(tid=thisClass['tid'])
    if not teacher.exists():
        return JsonResponse(2, safe=False)
    # 判断班级是否已存在
    sameClass = class_info.objects.filter(grade=thisClass['grade'])
    sameClass = sameClass.filter(cnumber=thisClass['class_num'])
    if sameClass.exists():
        return JsonResponse(1, safe=False)
    # 创建并保存班级数据
    newCid = "c{}{:0>2d}".format(int(thisClass['grade']), int(thisClass['class_num']))
    newClass = class_info.objects.create(cid=newCid, cnumber=thisClass['class_num'], grade=thisClass['grade'])
    # 关联班级与教师
    teacher_class.objects.create(cid=newClass, tid=teacher.first())

    return JsonResponse(0, safe=False)
    # return JsonResponse(-1,safe=False)


def login(request):
    """
    返回值:
    0 - 登陆成功
    1 - 登陆失败，密码错误
    2 - 登陆失败，账号不存在
    """
    account = request.POST['account']
    password = request.POST['password']
    print(account, password)
    findAccount = teacher_account.objects.filter(taccount=account)
    if findAccount:
        findAccount = findAccount.filter(tpassword=password)
    else:
        return JsonResponse({'rply': 2, 'teacherID': ''}, safe=False)
    if findAccount:
        return JsonResponse({'rply': 0, 'teacherID': findAccount.first().tid}, safe=False)
    else:
        return JsonResponse({'rply': 1, 'teacherID': ''}, safe=False)


def regist(request):
    """
    返回值:
    0 - 注册成功
    1 - 注册失败，账号已被注册
    2 - 注册失败，请输入有效的账号密码
    """
    if request.method == 'GET':
        return JsonResponse(-1, safe=False)
    account = request.POST['account']
    password = request.POST['password']
    print(account, password)
    if teacher_account.objects.filter(taccount=account).exists():
        return JsonResponse(1, safe=False)
    if account == '' or password == '':
        return JsonResponse(2, safe=False)

    # 系统创建tid
    AdminAccount = teacher_account.objects.filter(taccount='admin')
    newTid = AdminAccount.first().tid
    AdminTid = 't' + str(int(newTid[1:]) + 1)
    AdminAccount.update(tid=AdminTid)

    teacher_account.objects.create(tid=newTid, taccount=account, tpassword=password)
    return JsonResponse(0, safe=False)


def init_MainWindowP1(request):
    """
    返回值:
    {
        "class":[{"classID":,"studentNum":}{...}]
        "classNum":
        }
    """
    if request.method == 'GET':
        return JsonResponse(-1, safe=False)

    Tid = request.POST['tid']
    Tclass = teacher_class.objects.filter(tid=Tid)
    returnClassList = []
    for tclass in Tclass:
        stuNum = student_info.objects.filter(cid=tclass.cid).count()
        returnClassList.append({"classID": tclass.cid.cid, "studentNum": stuNum})
    classNum = Tclass.count()
    print('print from initDataP1:--------')
    print(returnClassList, classNum)
    return JsonResponse({"class": json.dumps(returnClassList), 'classNum': classNum}, safe=False)


def init_StudentData(request):
    """
    GET: -1
    POST: 
        PARA:
        {'cid':,'date':}
        RETURN:
        {
            'data':[{'sname':,'sid':,'totaltime','uptime':,'downtime':,'sleeptime':},{}...],
            }
    """
    # GET
    if request.method == 'GET':
        return JsonResponse(-1, safe=False)

    # POST
    reqCid = request.POST['cid']
    reqDate = request.POST['date']
    aimClass = class_info.objects.filter(cid=reqCid).first()
    aimStuList = student_info.objects.filter(cid=aimClass)
    returnList = []
    for stu in aimStuList:
        studata = student_daily_data.objects.filter(sid=stu)
        studata = studata.filter(date=reqDate)
        if not studata.exists():
            continue
        studata = studata.first()
        returnList.append({'sname': stu.sname, 'sid': stu.sid, 'totaltime': studata.totle_time,
                           'uptime': studata.up_time, 'downtime': studata.down_time, 'sleeptime': studata.sleep_time})
    print('print from initDataP2:--------')
    print(returnList)
    return JsonResponse({'data': json.dumps(returnList)}, safe=False)


# 上传学生照片
def post_student_picture(request):
    if request.method == 'POST':
        file = request.FILES['img']
        stu_id = request.POST['sid']
        # try:
        stu_cid = student_info.objects.filter(sid=stu_id).first().cid.cid
        print(stu_cid)
        # except:
        # return print('not find this student')

        # 创建文件夹

        try:
            File_Path = os.getcwd() + "\\" + 'img' + "\\" + stu_cid + "\\"
            print(File_Path)
            # 判断是否已经存在该目录
            if not os.path.exists(File_Path):
                # 目录不存在，进行创建操作
                os.makedirs(File_Path)  # 使用os.makedirs()方法创建多层目录
                print("目录新建成功：" + File_Path)
            else:
                print("目录已存在！！！")
        except BaseException as msg:
            print("新建目录失败：" + msg)
        print(file)
        student = student_info.objects.filter(sid=request.POST['sid']).first()
        # pic_path = 'D:\大三实训\pythonProject\mysite\学生照片\\'
        # pic_path = pic_path + stu_id + '.jpg'
        # print(pic_path)
        File_Path = File_Path + stu_id + '.jpg'
        # 判断该学生是否已有照片
        if os.path.exists(File_Path):
            os.remove(File_Path)
        path = default_storage.save(File_Path, ContentFile(file.read()))
        # print(request.POST['sid'])
        student_info.objects.filter(sid=request.POST['sid']).update(spic=File_Path)
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        class_id = student_info.objects.filter(sid=request.POST['sid']).first().cid.cid
        CCTV = class_info.objects.filter(cid=class_id).first().cctv.cctv
        old_update_num = ALLCCTV.objects.filter(cctv=CCTV).first().update_num
        while True:
            new_update_num = ''.join(
                str(i) for i in random.sample(range(0, 9), 5))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
            if (new_update_num != old_update_num):
                break
        ALLCCTV.objects.filter(cctv=CCTV).update(update_num=new_update_num)
        return JsonResponse('成功接收', safe=False)
    return JsonResponse('未成功接收', safe=False)


# 选择学生
def choose_stu_name(request):
    """
    PARA:
    {'data':[cid1,cid2]}
    RETURN:
        {'data':[sid-name1,sid-name2]}
    """
    classlist = json.loads(request.POST['data'])
    stu_list = []
    for classid in classlist:
        thisclass = class_info.objects.filter(cid = classid).first()
        cho = student_info.objects.filter(cid = thisclass)
        for sid_name in cho:
            sid_sname = sid_name.sname + " " + sid_name.sid
            stu_list.append(sid_sname)

    data = json.dumps(stu_list)
    return JsonResponse({'data': data})


# 导入学生名单
def import_stu_info(request):
    if request.method == 'POST':
        stu_info = json.loads(request.POST['data'])
        print(stu_info)
        for stu in stu_info:
            class_id = class_info.objects.filter(cid=stu['cid']).first()
            if student_info.objects.filter(sid=stu['sid']).exists():
                student_info.objects.filter(sid=stu['sid']).update(sname=stu['name'], cid=class_id)
            else:
                student_info.objects.create(sid=stu['sid'], sname=stu['name'], cid=class_id)

        return JsonResponse('成功接受', safe=False)
    return JsonResponse('未成功接受学生信息', safe=False)


def get_stu_daily_data(request):
    """
    POST:
        PARA:
        {'s20191571':json.dumps([0,0,0]),'s20192570':...}
    """
    now_date = datetime.date.today()
    if request.method == 'POST':
        daily_info = request.POST
        print(daily_info)
        for stu_id in daily_info:
            stu = student_info.objects.filter(sid=stu_id).first()
            stu_data = json.loads(daily_info[stu_id])
            student_daily_data.objects.create(date=now_date, sid=stu, up_time=stu_data[0], down_time=stu_data[1],
                                              sleep_time=stu_data[2],
                                              totle_time=stu_data[0] + stu_data[1] + stu_data[2])
        return JsonResponse('成功接收', safe=False)
    return JsonResponse('未成功接收每日数据', safe=False)


# 绑定班级监控
def bent_class_cctv(request):
    if request.method == 'POST':
        class_infomation = json.loads(request.POST['data'])
        print(class_infomation[0])
        CCTV = ALLCCTV.objects.filter(cctv=class_infomation[0]['cctv']).first()
        # print(class_info.objects.filter(cid=class_infomation[0]['class_id']))
        if class_info.objects.filter(cctv=CCTV).exists():
            return JsonResponse('1', safe=False)
        else:
            class_info.objects.filter(cid=class_infomation[0]['class_id']).update(cctv=CCTV)
            return JsonResponse('2', safe=False)
    return JsonResponse('未成功绑定', safe=False)


def choose_class(request):
    cho = class_info.objects.all()
    class_id_list = []
    for class_id in cho:
        class_id_list.append(class_id.cid)
    print(class_id_list)
    data = json.dumps(class_id_list)
    return JsonResponse({'data': data})


def choose_cctv(request):
    cho = ALLCCTV.objects.all()
    cctv_id_list = []
    for cctv_id in cho:
        cctv_id_list.append(cctv_id.cctv)
    data = json.dumps(cctv_id_list)
    return JsonResponse({'data': data})


def send_stu_pic(request):
    if request.method == 'POST':
        CCTV_term = request.POST
        if CCTV_term['old_update_num'] == ALLCCTV.objects.filter(cctv=CCTV_term['cctv']).first().update_num:
            return JsonResponse('not update student pic', safe=False)
        else:
            new_update_num = ALLCCTV.objects.filter(cctv=CCTV_term['cctv']).first().update_num
            CCTV = ALLCCTV.objects.filter(cctv=CCTV_term['cctv']).first()
            class_id = class_info.objects.filter(cctv=CCTV).first()
            stu_list = student_info.objects.filter(cid=class_id)
            print(stu_list)
            returnDict = {'update_num': new_update_num}
            for stu in stu_list:
                stu_sid = stu.sid
                stu_path = stu.spic
                print(stu_path)
                with open(stu_path, 'rb') as f:
                    image_byte = base64.b64encode(f.read())
                    image_str = image_byte.decode('ascii')
                    returnDict.update({stu_sid: image_str})
                    f.close()
        print(returnDict)
        return JsonResponse(returnDict)
    return 0
