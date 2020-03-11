import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from logindialog import Ui_login
from query import queryForm
import socket

class loginForm(QtWidgets.QWidget,Ui_login):
    def __init__(self):
        super(loginForm,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录页")
        self.setWindowIcon(QtGui.QIcon('res/myico.ico'))
        self.photolabel.setPixmap(QtGui.QPixmap('res/QQ.png'))
        self.photolabel.setScaledContents (True)  # 让图片自适应label大小
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap("res/login.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)
        #self.enter.setShortcut(QtCore.Qt.Key_Enter)
        self.id = ''
        #self.queryform = queryForm(self.id)
        self.enter.clicked.connect(self.jump_query)
        #上次记住的密码
        if (os.path.isfile('inifiles/default.txt') and os.path.getsize('inifiles/default.txt')!=0):
            with open('inifiles/default.txt', "r") as fr:
                inimes=fr.readlines()
                self.usrline.setText(inimes[0].strip('\n'))
                self.pasdline.setText(inimes[1])


    def connect_Middle_Server(self):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((servername, serverPort))#与服务器建立连接
            sentence = self.usrline.text() + '_' + self.pasdline.text()
            str_usr = self.usrline.text()
            clientSocket.send(sentence.encode())
            mes_return = clientSocket.recv(2048)
            clientSocket.close()
            if (mes_return.decode() == "lol"):
                self.id = self.usrline.text()
                with open('inifiles/default.txt', 'a+')as g:#记住密码存储在资源文件
                    g.seek(0)
                    g.truncate()
                    if (self.checkBox.isChecked()):
                        g.writelines(self.usrline.text() + "\n")
                        g.writelines(self.pasdline.text())
                    g.close()
                return True
            else:
                QtWidgets.QMessageBox.about(self, "提示", "用户名或密码错误！")
                return False
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "提示", "无法连接服务器！")
            return False

    def jump_query(self):
        if(self.connect_Middle_Server()==True):
            queryform=queryForm(self.id)  #登陆成功，打开主页
            queryform.show()
            self.close()
            queryform.exec_()

if __name__ == '__main__':
    servername = '166.111.140.57'
    serverPort = 8000
    app = QtWidgets.QApplication(sys.argv)
    my_form = loginForm()
    my_form.show()
    #my_form.setFixedSize(980,600)
    #my_form.use_palette()
    sys.exit(app.exec_())

