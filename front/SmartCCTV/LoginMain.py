import Ui_login as login
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import WindowMain
import requests
import json
from qt_material import apply_stylesheet
# back program port
localhost = 'http://127.0.0.1:8000/'


class login_window(login.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(login_window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.change_widget2)
        self.pushButton_2.clicked.connect(self.change_widget3)
        self.widget_3.hide()

        self.pushButton_3.clicked.connect(self.buttonFuc3)
        self.pushButton_4.clicked.connect(self.buttonFuc4)

        self.app = QApplication(sys.argv)
        self.win = WindowMain.pages_window()

    def printMessageBox(self, titlelist, messagelist, rply):
        """ez Message Box"""
        if rply < 0 or rply >= len(titlelist):
            QMessageBox.information(self, '错误', '未知错误', QMessageBox.Yes, QMessageBox.Yes)
            return
        QMessageBox.information(self, titlelist[rply], messagelist[rply], QMessageBox.Yes, QMessageBox.Yes)

    def buttonFuc3(self):
        # 登录功能
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()
        # 上传
        url = localhost + 'login/'
        req = requests.post(url, {'account': account, 'password': password})
        # 读取返回值
        rply = json.loads(req.text)['rply']
        self.printMessageBox(['成功', '失败', '失败'], ['登录成功', '密码错误', '账号不存在'], rply)
        if rply == 0:
            self.close()
            self.win.saveTeacherID(json.loads(req.text)['teacherID'])
            self.win.initData()
            self.win.lineEdit_4.setReadOnly(True)
            self.win.lineEdit_4.setText(self.win.teacherID)
            self.win.lineEdit_5.setReadOnly(True)
            self.win.lineEdit_5.setText(self.win.teacherID)
            self.win.lineEdit_6.setReadOnly(True)
            self.win.lineEdit_6.setText(self.win.teacherID)
            # apply_stylesheet(self.win,theme='dark_teal.xml')
            self.win.show()

    def buttonFuc4(self):
        # 注册功能
        account = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        # 上传
        url = localhost + 'regist/'
        req = requests.post(url, {'account': account, 'password': password})
        rply = json.loads(req.text)
        self.printMessageBox(['成功', '失败', '失败'], ['注册成功', '账号已存在', '请输入合规的账号密码'], rply)


    def change_widget2(self):
        self.widget_3.hide()
        self.widget_2.show()

    def change_widget3(self):
        self.widget_2.hide()
        self.widget_3.show()


def runLogin():
    app = QApplication(sys.argv)
    loginUi = login_window()

    loginUi.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    runLogin()
