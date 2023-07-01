import login
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    loginUi = login.Ui_MainWindow()
    loginUi.setupUi(win)
    loginUi.widget_3.hide()


    def change_widget3():
        loginUi.widget_2.hide()
        loginUi.widget_3.show()


    def change_widget2():
        loginUi.widget_3.hide()
        loginUi.widget_2.show()


    loginUi.pushButton.clicked.connect(change_widget2)
    loginUi.pushButton_2.clicked.connect(change_widget3)
    win.show()
    sys.exit(app.exec_())
