import Main
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class pages_window(Main.Ui_MainWindow,QMainWindow):
    def __init__(self):
        super(pages_window,self).__init__()
        self.setupUi(self)
        #点击左侧第一个按钮切换到第一个页面
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
        self.stackedWidget.setCurrentIndex(0)


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

if __name__ == '__main__':
     app = QApplication(sys.argv)
     win = pages_window()
     win.show()
     sys.exit(app.exec_())



