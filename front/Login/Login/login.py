# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1109, 901)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 210, 391, 591))
        self.label.setStyleSheet("border-radius:30px;\n"
                                 "background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(350, 360, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(420, 240, 121, 111))
        self.label_3.setStyleSheet("image: url(:/icons/icons/电脑_computer.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(380, 400, 215, 50))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("#pushButton{\n"
                                      "    border:none;\n"
                                      "}\n"
                                      "#pushButton:focus{\n"
                                      "    color: rgb(186, 186, 186);\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
                                        "    border:none;\n"
                                        "}\n"
                                        "#pushButton_2:focus{\n"
                                        "    color: rgb(186, 186, 186);\n"
                                        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(280, 470, 391, 311))
        self.widget_2.setObjectName("widget_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(70, 40, 261, 41))
        self.lineEdit.setStyleSheet("border:1px solid rgb(0,0,0);\n"
                                    "border-radius:8px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 140, 261, 41))
        self.lineEdit_2.setStyleSheet("border:1px solid rgb(0,0,0);\n"
                                      "border-radius:8px;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 230, 271, 31))
        self.pushButton_3.setStyleSheet("#pushButton_3{\n"
                                        "    border-radius:8px;\n"
                                        "    background-color: rgb(0, 0, 0);\n"
                                        "    color: rgb(255, 255, 255);\n"
                                        "    border:3px solid rgb(0,0,0);\n"
                                        "\n"
                                        "}\n"
                                        "#pushButton_3:hover{\n"
                                        "    \n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "    color: rgb(0, 0, 0);\n"
                                        "}\n"
                                        "#pushButton_3:pressed{\n"
                                        "    padding-top:5px;\n"
                                        "    padding-left:5px;\n"
                                        "}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 220, 21, 16))
        self.pushButton_5.setStyleSheet("#pushButton_5{\n"
                                        "    image: url(:/icons/icons/关闭_close-one.png);\n"
                                        "    border:none;\n"
                                        "}")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(280, 450, 391, 311))
        self.widget_3.setObjectName("widget_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(70, 60, 261, 41))
        self.lineEdit_3.setStyleSheet("border:1px solid rgb(0,0,0);\n"
                                      "border-radius:8px;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(70, 160, 261, 41))
        self.lineEdit_4.setStyleSheet("border:1px solid rgb(0,0,0);\n"
                                      "border-radius:8px;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_4.setGeometry(QtCore.QRect(70, 250, 271, 31))
        self.pushButton_4.setStyleSheet("#pushButton_4{\n"
                                        "    border-radius:8px;\n"
                                        "    background-color: rgb(0, 0, 0);\n"
                                        "    color: rgb(255, 255, 255);\n"
                                        "    border:3px solid rgb(0,0,0);\n"
                                        "\n"
                                        "}\n"
                                        "#pushButton_4:hover{\n"
                                        "    \n"
                                        "    background-color: rgb(255, 255, 255);\n"
                                        "    color: rgb(0, 0, 0);\n"
                                        "}\n"
                                        "#pushButton_4:pressed{\n"
                                        "    padding-top:5px;\n"
                                        "    padding-left:5px;\n"
                                        "}")
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.pushButton_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.pushButton_4.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.retranslateUi(MainWindow)
        self.pushButton_5.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "教室智能监控与分析系统"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "注册"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "账号："))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "密码："))
        self.pushButton_3.setText(_translate("MainWindow", "登录"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "账号：输入教职工号"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "密码：6-12位数字和英文字母组成"))
        self.pushButton_4.setText(_translate("MainWindow", "注册"))


import resource
