import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets,QtGui,QtCore
from groupdialog import Ui_chatDialog
import threading
import socket
import win32ui
from file import fileForm

servername = '166.111.140.57'
serverPort = 8000

class groupForm(QtWidgets.QDialog,Ui_chatDialog):
    def __init__(self,connect,usr,group_id,group_friend):
        super(groupForm,self).__init__()
        self.setupUi(self)
        self.usr = usr
        self.group_id = group_id
        self.group_friend = group_friend
        self.connect = connect
        self.name = "群组" + group_id
        self.setWindowTitle(self.name)
        self.setWindowIcon(QtGui.QIcon('res/myico.ico'))
        self.top_label.setPixmap(QtGui.QPixmap('res/top.jpg'))
        self.loadchat()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((servername, serverPort))
        #self.sendmes.clicked.connect(self.sendmessage)
        #self.loadchat()
        statelist = []
        for person in self.group_friend:
            sentence = 'q' + person
            self.clientSocket.send(sentence.encode())
            mes_return = self.clientSocket.recv(2048)
            if (mes_return.decode() == 'n'):
                statelist.append("离线")
            else:
                statelist.append("在线")

        self.tableWidget.setFrameShape(0)
        # self.tableWidget.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setRowCount(len(self.group_friend))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['群成员', '在线状态'])
        self.tableWidget.verticalHeader().setHidden(True)
        i = j = 0
        for person in self.group_friend:
            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(person))
            j = j + 1
            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(statelist[i]))
            i = i + 1
            j = 0
        self.sendmes.clicked.connect(self.sendmessage)
        self.lookstate.clicked.connect(self.searchstate)
        # 新建线程监听收到新消息更新界面
        self.connect.revgroup_Signal.connect(self.updatechat)
        self.connect.group_process_Signal.connect(self.updaterevpro)
        self.upfile.clicked.connect(self.uploadchoose)
        self.sedfilepro_Signal.connect(self.updatesedpro)
        self.file.clicked.connect(self.lookfile)

    sedfilepro_Signal = QtCore.pyqtSignal(int)
    group_Signal = QtCore.pyqtSignal(str)

    def closeEvent(self, event):
        self.group_Signal.emit('1')

    def loadchat(self):
        i = 0
        #self.textBrowser.setText("")
        if (os.path.isfile('users/' + self.usr + '/' + self.group_id + ".txt")):
            with open('users/' + self.usr + '/' + self.group_id + ".txt", "r") as fr:
                # all_lines = len(fr.readlines())
                # if(all_lines > num):
                for line in fr.readlines():
                    #将本人的话显示在右，好友的话显示在左
                    i = i + 1
                    if(i%2 == 1):
                        if (line[0:10] != self.usr):
                            self.textBrowser.setAlignment(QtCore.Qt.AlignLeft)
                        else:
                            self.textBrowser.setAlignment(QtCore.Qt.AlignRight)
                    self.textBrowser.append(line)
                # num = all_lines
                self.cursor = self.textBrowser.textCursor()
                self.textBrowser.moveCursor(self.cursor.End)
                #time.sleep(1)

    def updatechat(self,rev_Str):
        if(rev_Str[0]!=self.usr and rev_Str[3]==str(6)):
            self.textBrowser.append('\n')
            self.textBrowser.setAlignment(QtCore.Qt.AlignLeft)
            self.textBrowser.append(rev_Str[0] + " " + rev_Str[1])
            self.textBrowser.append('\n')
            self.textBrowser.append(rev_Str[2].split("$")[0])
            self.cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursor.End)

    def searchstate(self):
        statelist = []
        for person in self.group_friend:
            sentence = 'q' + person
            self.clientSocket.send(sentence.encode())
            mes_return = self.clientSocket.recv(2048)
            if (mes_return.decode() == 'n'):
                statelist.append("离线")
            else:
                statelist.append("在线")
        i = j = 0
        for person in self.group_friend:
            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(person))
            j = j + 1
            self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(statelist[i]))
            i = i + 1
            j = 0

    def sendmessage(self):
        word = self.lineEdit.text()
        if (word == ""):
            QtWidgets.QMessageBox.about(self, "提示", "不能发送空消息！")
        else:
            for friend in self.group_friend:
                sentence = 'q' + friend
                self.clientSocket.send(sentence.encode())
                frimes_return = self.clientSocket.recv(2048).decode()
                if(frimes_return!="n"):
                    self.connect.SendMessage(self.usr,friend,frimes_return,word+"$"+self.group_id,6) #群聊消息与群聊ID用$分隔
            data = QtCore.QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd-hh:mm")
            self.textBrowser.append('\n')
            self.textBrowser.setAlignment(QtCore.Qt.AlignRight)
            self.textBrowser.append(self.usr + " " + currTime)
            self.textBrowser.append('\n')
            self.textBrowser.append(word)
            self.cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursor.End)
            self.lineEdit.setText("")

    def updaterevpro(self,rev_int):
        if(rev_int == 0):
            self.filestate.setText("文件接收中...")
        elif(rev_int == 1):
            self.filestate.setText("文件接收完毕")

    def updatesedpro(self,rev_int):
        if (rev_int == 0):
            self.filestate.setText("文件传输中...")
        elif (rev_int == 1):
            self.filestate.setText("文件传输完毕")
            data = QtCore.QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd-hh:mm")
            self.textBrowser.append('\n')
            self.textBrowser.setAlignment(QtCore.Qt.AlignRight)
            self.textBrowser.append(self.usr + " " + currTime)
            self.textBrowser.append('\n')
            self.textBrowser.append("成功发送文件" + self.filename)
            self.cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursor.End)

    def uploadchoose(self):
        self.upfilethread = threading.Thread(target=self.uploadfile)
        self.upfilethread.start()

    def open_file(self):
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        dlg.SetOFNInitialDir('C://')  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        filename = dlg.GetPathName()  # 获取选择的文件名称
        return filename

    def uploadfile(self):
        try:
            filename = self.open_file()
            # root = tkinter.Tk()
            # root.withdraw()
            # filename = tkinter.filedialog.askopenfilename()
            print(filename)
            file_name = filename.split('\\')
            self.filename = file_name[-1]
            if(self.filename !=""):
                filesize = os.path.getsize(filename)  # 得到文件的大小,字节
                print(filesize)
                dirc = {'filename': filename, 'filesize': filesize, 'group_id': self.group_id}
                self.sedfilepro_Signal.emit(0)
                for friend in self.group_friend:
                    sentence = 'q' + friend
                    self.clientSocket.send(sentence.encode())
                    frimes_return = self.clientSocket.recv(2048).decode()
                    if (frimes_return != "n"):
                        self.connect.SendMessage(self.usr, friend, frimes_return, dirc, 7)
                        self.connect.SendMessage(self.usr, friend, frimes_return,
                                                 "成功发送文件" + file_name[-1] + "$" + self.group_id, 6)
                self.sedfilepro_Signal.emit(1)
            #stop_thread(self.upfilethread)
        except Exception as e:
            print(e)

    def lookfile(self):
        self.fileform = fileForm(self.usr, self.group_id)
        self.fileform.show()