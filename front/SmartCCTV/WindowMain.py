from this import s
from tkinter import filedialog

from matplotlib import pyplot as plt
import Ui_Main
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap
import requests
import json
# import pyqtgraph
import numpy
from tkinter import Tk, filedialog
import datetime
import xlrd as xlrd
import numpy as np
from qt_material import apply_stylesheet

# back program port
localhost = 'http://127.0.0.1:8000/'


class pages_window(Ui_Main.Ui_MainWindow, QMainWindow):
    def __init__(self):
        # 用于存储登录账号的教师id
        self.teacherID = 't10000'
        # 用于存储教师的班级及各班级的学生人数
        self.classList = []  # ['c201913','c201918',...]
        self.stuNum = []  # [3,2,...]
        # --------------------------------------------------------
        super(pages_window, self).__init__()
        self.setupUi(self)
        # 点击左侧第一个按钮切换到第一个页面
        self.pushButton.clicked.connect(self.display_page)
        # 点击左侧第二个按钮切换到第二个页面
        self.pushButton_2.clicked.connect(self.display_page2)
        # 点击左侧第三个按钮切换到第三个页面
        self.pushButton_3.clicked.connect(self.display_page3)
        # 点击左侧第四个按钮切换到第四个页面
        self.pushButton_4.clicked.connect(self.display_page4)
        # 点击左侧第五个按钮切换到第五个页面
        self.pushButton_5.clicked.connect(self.display_page5)
        # 点击左侧第六个按钮切换到第六个页面
        self.pushButton_6.clicked.connect(self.display_page6)
        # 点击第八个按钮(教师信息录入页的保存)
        self.pushButton_8.clicked.connect(self.buttonFuc8)
        # 点击第十四个按钮(班级创建页面的保存)
        self.pushButton_14.clicked.connect(self.buttonFuc14)
        # 点击第十五个按钮(学生列表界面的切换班级按钮)
        self.pushButton_15.clicked.connect(self.buttonFuc15)
        # 点击第七个按钮(班级概况页面的切换班级按钮)
        self.pushButton_7.clicked.connect(self.buttonFuc7)
        self.stackedWidget.setCurrentIndex(0)

        # 导入学生名单
        self.pushButton_9.clicked.connect(self.open)
        # 将学生名单添加至下拉栏
        self.pushButton_16.clicked.connect(self.refresh)
        # 导入学生照片
        self.pushButton_10.clicked.connect(self.post_students_picture)

        # -----------------------------test code---------------------------------
        self.label_27.setPixmap(QPixmap('tempImg/saveBar.jpg'))
        self.label_27.setScaledContents(True)
        # -----------------------------bent--------------------------------------
        self.pushButton_12.clicked.connect(self.bent_clss_cctv)
        # -------------------------------end test--------------------------------

        # self.tableWidget.setItem(0,0,QTableWidgetItem("haha"))
        # 初始化combobox
        # init comboBox_4
        grade_list = ['2019', '2020', '2021', '2022']
        self.comboBox_4.addItems(grade_list)
        self.comboBox.addItems(['1', '2', '3', '4'])

    def tableSetRow(self, table, contentList, row):
        i = 0
        for content in contentList:
            table.setItem(row, i, QTableWidgetItem(str(content)))
            i = i + 1

    def saveTeacherID(self, tid):
        # 登陆成功后存储登陆账号的tid
        self.teacherID = tid

    def initData(self):
        # 初始化班级页面的学生总数P1
        tid = self.teacherID
        print(tid)
        url = localhost + 'initDataP1/'
        req = requests.post(url, {'tid': tid})
        classNum = json.loads(req.text)['classNum']
        classList = json.loads(json.loads(req.text)['class'])
        print('classlist----------------------------------------')
        print(self.classList)
        #print(classNum, classList)
        self.textBrowser_2.setText(str(classNum))
        if classList:
            self.textBrowser.setText(str(classList[0]['studentNum']))
        # 初始化切换班级位置的下拉菜单
        self.comboBox_5.clear()
        for item in classList:
            self.comboBox_5.addItem(item['classID'])
        # 将数据保存在self中
        self.classList.clear()
        for aClass in classList:
            self.classList.append(aClass['classID'])
            self.stuNum.append(aClass['studentNum'])
        print(self.classList, self.stuNum)
        # ----------------------------------------------------------
        # 初始化学生列表P2
        if classList:
            url = localhost + 'initStudentData/'
            req = requests.post(url, {'cid': self.classList[0], 'date': datetime.date.today()+ datetime.timedelta(days=-1)})
            print(self.classList[0])
            dataList = json.loads(json.loads(req.text)['data'])
            print(dataList)
            self.tableWidget.setRowCount(len(dataList))
            # 初始化学生列表
            i = 0
            for data in dataList:
                self.tableSetRow(self.tableWidget, [data['sname'], data['sid'],
                                                    data['totaltime'], data['uptime'], data['downtime'],
                                                    data['sleeptime']], i)
                i = i + 1
            # 初始化切换班级combobox
            self.comboBox_6.clear()
            self.comboBox_6.addItems(self.classList)

            # ---------------------------------------------------
            self.generateGraphics(self.classList[0])
            self.label_27.setPixmap(QPixmap('tempImg/saveLine.jpg'))
            self.label_27.setScaledContents(True)
            self.label_30.setPixmap(QPixmap('tempImg/saveBar.jpg'))
            self.label_30.setScaledContents(True)
            self.label_45.setPixmap(QPixmap('tempImg/saveCake.jpg'))
            self.label_45.setScaledContents(True)
            #

            # --------------------------------------------------------
            url_3 = 'http://127.0.0.1:8000/sid_sname/choose/'

            req = requests.post(url_3,{'data':json.dumps(self.classList)})
            stu_list = json.loads(json.loads(req.text)['data'])
            # print(stu_list)
            self.comboBox.clear()
            self.comboBox.addItems(stu_list)
            # 将班级添加至下拉栏
            url_1 = 'http://127.0.0.1:8000/class/choose/'
            req_1 = requests.get(url_1)
            class_id = json.loads(json.loads(req_1.text)['data'])
            # print(class_id)
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.classList)
            # 将监控编号添加至下拉栏
            url_2 = 'http://127.0.0.1:8000/cctv/choose/'
            req_2 = requests.get(url_2)
            cctv_id = json.loads(json.loads(req_2.text)['data'])
            print(cctv_id)
            self.comboBox_3.clear()
            self.comboBox_3.addItems(cctv_id)
            self.label_16.clear()

    def generateGraphics(self, classID):
        print("#generating Graphics------------")
        datelist = []
        tempdate = datetime.date.today()
        for i in range(7):
            tempdate = tempdate + datetime.timedelta(days=-1)
            datelist.append(tempdate)
        url = localhost + 'initStudentData/'
        allData = []
        for i in range(7):
            req = requests.post(url, {'cid': classID, 'date': datelist[i]})
            allData.append(json.loads(json.loads(req.text)['data']))

        print(allData)
        # 通过学生数据生成图片
        # 生成折线图------------------------------------------------------
        line_x = []
        line_y1 = []
        line_y2 = []
        line_y3 = []

        for i in range(7):
            if allData[i]:
                line_x.append(str(datelist[i]))
                uptemp = 0
                downtemp = 0
                sleeptemp = 0
                for stu in allData[i]:
                    uptemp = uptemp + stu['uptime']
                    downtemp = downtemp + stu['downtime']
                    sleeptemp = sleeptemp + stu['sleeptime']
                line_y1.append(uptemp / len(allData[i]))
                line_y2.append(downtemp / len(allData[i]))
                line_y3.append(sleeptemp / len(allData[i]))
        line_x.reverse()
        line_y1.reverse()
        line_y2.reverse()
        line_y3.reverse()

        plt.clf()
        plt.title(classID + ' Average Data')
        plt.grid(linestyle=":")
        plt.plot(line_x, line_y1, label='up_time')
        plt.plot(line_x, line_y2, label='down_time')
        plt.plot(line_x, line_y3, label='sleep_time')
        plt.legend(loc=1)
        plt.subplots_adjust(wspace=0.2, hspace=0.4)
        plt.tight_layout()
        plt.savefig('tempImg/saveLine.jpg')

        print(line_y1, line_y2, line_y3, line_x)

        # 生成柱形图-------------------------------------------------
        bar_x = []
        bar_y1 = []
        bar_y2 = []
        bar_y3 = []
        templist = []  # use for sort
        # rebuild dict for sort
        for stu in allData[0]:
            score = stu['uptime'] * 2 + stu['downtime'] * 1
            templist.append({'sname': stu['sname'], 'uptime': stu['uptime'], 'downtime': stu['downtime'],
                             'sleeptime': stu['sleeptime'], 'score': score})
        sorted_dict = sorted(templist, key=lambda x: x['score'], reverse=True)
        print(sorted_dict)

        # 显示最高的前7位学生
        lenth = len(templist)
        for i in range(7):
            if i >= lenth:
                break
            bar_x.append(templist[i]['sname'])
            bar_y1.append(templist[i]['uptime'])
            bar_y2.append(templist[i]['downtime'])
            bar_y3.append(templist[i]['sleeptime'])

        plt.clf()
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(10, 8))
        plt.bar(bar_x, bar_y1, label='抬头时长', width=0.5, bottom=0, linewidth=2)
        plt.bar(bar_x, bar_y2, label='低头时长', bottom=bar_y1, width=0.5, linewidth=2)
        plt.bar(bar_x, bar_y3, label='趴下时长', bottom=np.sum([bar_y1, bar_y2], axis=0), width=0.5, linewidth=2)
        plt.legend(loc=1)
        plt.title(classID + ' score Top 6')
        plt.savefig('tempImg/saveBar.jpg')

        # 生成饼状图
        plt.clf()
        cake_x1 = sum(line_y1)
        cake_x2 = sum(line_y2)
        cake_x3 = sum(line_y3)
        x = np.array([cake_x1, cake_x2, cake_x3])
        plt.pie(x,
                labels=['up_time', 'down_time', 'sleep_time'],
                # 设置饼图标签，以列表形式传入
                )
        plt.title(classID + " Total Time")
        plt.savefig('tempImg/saveCake.jpg')

    def printMessageBox(self, titlelist, messagelist, rply):
        if rply < 0 or rply >= len(titlelist):
            QMessageBox.information(self, '错误', '未知错误', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        QMessageBox.information(self, titlelist[rply], messagelist[rply], QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.Yes)

    def buttonFuc15(self):
        url = localhost + 'initStudentData/'
        reqCid = self.comboBox_6.currentText()
        req = requests.post(url, {'cid': reqCid, 'date': datetime.date.today()+ datetime.timedelta(days=-1)})
        dataList = json.loads(json.loads(req.text)['data'])
        print(dataList)
        self.tableWidget.setRowCount(len(dataList))
        # 修改学生列表
        i = 0
        for data in dataList:
            self.tableSetRow(self.tableWidget, [data['sname'], data['sid'],
                                                data['totaltime'], data['uptime'], data['downtime'], data['sleeptime']],
                             i)
            i = i + 1

    def buttonFuc8(self):
        name = self.lineEdit.text()
        school = self.lineEdit_2.text()
        sex = self.lineEdit_3.text()
        tid = self.lineEdit_4.text()
        url = localhost + "saveinfo/teacher/"
        req = requests.post(url, {'name': name, 'school': school, 'sex': sex, 'tid': tid})
        rply = json.loads(req.text)
        self.printMessageBox(['成功', '失败', '失败'],
                             ['信息创建成功', '信息修改成功', '未找到该教师，请检查教师号'], rply)

    def buttonFuc7(self):
        nowclass = self.comboBox_5.currentText()
        self.generateGraphics(nowclass)
        self.label_27.setPixmap(QPixmap('tempImg/saveLine.jpg'))
        self.label_27.setScaledContents(True)
        self.label_30.setPixmap(QPixmap('tempImg/saveBar.jpg'))
        self.label_30.setScaledContents(True)
        self.label_45.setPixmap(QPixmap('tempImg/saveCake.jpg'))
        self.label_45.setScaledContents(True)

    def buttonFuc14(self):
        tid = self.lineEdit_6.text()
        grade = self.comboBox_4.currentText()
        class_num = self.lineEdit_7.text()
        # test getting data from client
        # print(tid,grade,class_num)

        # interact with back program
        url = localhost + 'saveinfo/createClass/'
        req = requests.post(url, {'tid': tid, 'grade': grade, 'class_num': class_num})
        rply = json.loads(req.text)
        self.printMessageBox(['成功', '失败', '失败'],
                             ['信息创建成功', '班级已存在，请勿重复创建', '未找到教师，请检查教师编号'], rply)

    # #将学生名单刷新并加至下拉栏
    def set_refresh(self):
        url = 'http://127.0.0.1:8000/sid_sname/choose/'
        req = requests.get(url)
        stu_list = json.loads(json.loads(req.text)['data'])
        # print(stu_list)
        self.comboBox.clear()
        self.comboBox.addItems(stu_list)
        # 将班级添加至下拉栏
        url_1 = 'http://127.0.0.1:8000/class/choose/'
        req_1 = requests.get(url_1)
        class_id = json.loads(json.loads(req_1.text)['data'])
        # print(class_id)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(class_id)
        # 将监控编号添加至下拉栏
        url_2 = 'http://127.0.0.1:8000/cctv/choose/'
        req_2 = requests.get(url_2)
        cctv_id = json.loads(json.loads(req_2.text)['data'])
        print(cctv_id)
        self.comboBox_3.clear()
        self.comboBox_3.addItems(cctv_id)

        # 导入学生名单

    # 打开文件
    def open(self):
        Tk().withdraw()
        f_path = filedialog.askopenfilename()
        print('\n获取的文件地址：', f_path)
        try:
            readfile = xlrd.open_workbook(f_path)
        except:
            print('not open')
            QMessageBox.information(self, '提示', '表格存在班级号未创建！', QMessageBox.Yes, QMessageBox.Yes)
            return
        table = readfile.sheets()[0]
        row_num = table.nrows
        datalist = []
        print(row_num)
        try:
            for i in range(1, row_num):
                datalist.append(
                    {'sid': table.row_values(i)[0], 'name': table.row_values(i)[1], 'cid': table.row_values(i)[2]})
            url = 'http://127.0.0.1:8000/stu_info/save/'
            req = requests.post(url, {'data': json.dumps(datalist)})
            ans = json.loads(req.text)
            QMessageBox.information(self, '提示', '学生名单导入成功！', QMessageBox.Yes, QMessageBox.Yes)
            print(ans)
        except:
            QMessageBox.information(self, '提示', '表格存在班级号未创建！', QMessageBox.Yes, QMessageBox.Yes)

    # 上传学生照片
    def post_students_picture(self):
        url = 'http://127.0.0.1:8000/student_picture/post/'
        stu_name = self.comboBox.currentText().split()
        if stu_name == []:
            QMessageBox.information(self, '错误', '请选择学生', QMessageBox.Yes, QMessageBox.Yes)
            return
        sid = stu_name[len(stu_name) - 1]
        print(stu_name)
        # 获取照片路径
        Tk().withdraw()
        f_path = filedialog.askopenfilename()
        # readfile = Image.open(f_path)
        # files={'img':()}
        # req=requests.request('POST',url,)
        path_name = f_path.split('/')
        # upload_pic = {"files": ('path_name[len(path_name)]-1', open(f_path, 'rb'), 'image/jpeg', {})}
        # req = requests.post(url, files=upload_pic, data={"sid": "sid"})
        self.label_16.setPixmap(QPixmap(f_path))
        self.label_16.setScaledContents(True)  # 图片大小与label适应，否则图片可能显示不全
        # 传照片
        try:
            files = {'img': ('path_name[len(path_name)]-1', open(f_path, 'rb'), 'image/png')}
        except:
            print('not open')
            return
        data = {"sid": sid}
        req = requests.post(url, data=data, files=files)
        QMessageBox.information(self, '提示', '学生照片上传成功！', QMessageBox.Yes, QMessageBox.Yes)
        print(json.loads(req.text))

    # 绑定班级监控
    def bent_clss_cctv(self):
        clss_id = self.comboBox_2.currentText()
        cctv = self.comboBox_3.currentText()
        url = 'http://127.0.0.1:8000/bent/cctv/'
        datalist = [{'class_id': clss_id, 'cctv': cctv}]
        req = requests.post(url, {'data': json.dumps(datalist)})
        ans = json.loads(json.loads(req.text))
        if ans == 1:
            QMessageBox.information(self, '提示', '请勿重复绑定监控！', QMessageBox.Yes, QMessageBox.Yes)
        if ans == 2:
            QMessageBox.information(self, '提示', '班级监控绑定成功！', QMessageBox.Yes, QMessageBox.Yes)
        print(ans)


    #刷新
    def refresh(self):
        self.initData()
        QMessageBox.information(self,'提示','刷新系统成功',QMessageBox.Yes, QMessageBox.Yes)


    def display_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def display_page2(self):
        self.stackedWidget.setCurrentIndex(1)

    def display_page3(self):
        self.stackedWidget.setCurrentIndex(2)

    def display_page4(self):
        self.stackedWidget.setCurrentIndex(3)

    def display_page5(self):
        self.stackedWidget.setCurrentIndex(4)

    def display_page6(self):
        self.stackedWidget.setCurrentIndex(5)


def runWindow():
    app = QApplication(sys.argv)
    win = pages_window()
    win.generateGraphics('c201914')
    apply_stylesheet(win, theme='dark_teal.xml')
    win.show()
    sys.exit(app.exec_())






if __name__ == '__main__':
    app = runWindow()
