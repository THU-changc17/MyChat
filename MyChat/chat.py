import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets,QtGui,QtCore
from chatdialog import Ui_chatDialog
from file import fileForm
from P2Pconnect import P2Pconnect
import tkinter
from tkinter import filedialog
import threading
from threading import Thread
import time
import win32ui
import os
import pyaudio
import inspect
import ctypes
import json
import struct

class chatForm(QtWidgets.QDialog,Ui_chatDialog):
    def __init__(self,connect,usr,friend,usrIP,friendIP):
        super(chatForm,self).__init__()
        self.setupUi(self)
        self.usr = usr
        self.friend = friend
        self.usrIP = usrIP
        self.friendIP = friendIP
        self.connect = connect
        self.filename = ""
        #self.usrport = int('5' + usr[-4:])
        #self.friendport = int('5' + friend[-4:])
        self.name = self.usr + " 和 " + self.friend + "的聊天"
        self.setWindowTitle(self.name)
        self.setWindowIcon(QtGui.QIcon('res/myico.ico'))
        self.photolabel.setPixmap(QtGui.QPixmap('res/personal.jpg'))
        self.top_label.setPixmap(QtGui.QPixmap('res/top.jpg'))
        self.sendmes.clicked.connect(self.sendmessage)
        #self.connect = P2Pconnect(self.usr,self.friend,self.usrIP,self.friendIP)
        #self.connect.StartListen()
        #self.loadthread = threading.Thread(target=self.loadchat)
        #self.loadthread.start()
        self.loadchat()
        self.sedfilepro_Signal.connect(self.updatesedpro)
        self.connect.rev_Signal.connect(self.updatechat)
        self.connect.process_Signal.connect(self.updaterevpro)
        #self.send_pro_Signal.connect(self.send_sedpro_Signal)
        self.upfile.clicked.connect(self.uploadchoose)
        #self.progressBar.setValue(0)
        self.file.clicked.connect(self.lookfile)
        #self.audiochoose.clicked.connect(self.audiochat)

    my_Signal = QtCore.pyqtSignal(str)
    sedfilepro_Signal = QtCore.pyqtSignal(int)
    #重写关闭界面操作，向主页发送提示
    def closeEvent(self, event):
        self.my_Signal.emit('1')

    def updatechat(self,rev_Str):
        if (rev_Str[0] == self.friend and rev_Str[3] == str(2)):
            self.textBrowser.append('\n')
            self.textBrowser.setAlignment(QtCore.Qt.AlignLeft)
            self.textBrowser.append(rev_Str[0] + " " + rev_Str[1])
            self.textBrowser.append('\n')
            self.textBrowser.append(rev_Str[2])
            self.cursor = self.textBrowser.textCursor()
            self.textBrowser.moveCursor(self.cursor.End)

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

    def open_file(self):
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        dlg.SetOFNInitialDir('C://')  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        filename = dlg.GetPathName()  # 获取选择的文件名
        return filename

    def uploadchoose(self):
        self.upfilethread = threading.Thread(target=self.uploadfile)
        self.upfilethread.start()

    def uploadfile(self):
        try:
            filename = self.open_file()
            # root = tkinter.Tk()
            # root.withdraw()
            # filename = tkinter.filedialog.askopenfilename()
            print(filename)
            file_name = filename.split('\\')
            self.filename = file_name[-1]
            if(self.filename!=""):
                filesize = os.path.getsize(filename)  # 得到文件的大小,字节
                print(filesize)
                dirc = {'filename': filename, 'filesize': filesize}
                self.sedfilepro_Signal.emit(0)
                self.connect.SendMessage(self.usr, self.friend, self.friendIP, dirc, 4)
                self.connect.SendMessage(self.usr, self.friend, self.friendIP, "成功发送文件" + file_name[-1], 2)
                self.sedfilepro_Signal.emit(1)
            #stop_thread(self.upfilethread)
        except Exception as e:
            print(e)

    def lookfile(self):
        self.fileform = fileForm(self.usr, self.friend)
        self.fileform.show()

    def loadchat(self):
        i = 0
        #self.textBrowser.setText("")
        if (os.path.isfile('users/' + self.usr + '/' + self.friend + ".txt")):
            with open('users/' + self.usr + '/' + self.friend + ".txt", "r") as fr:
                # all_lines = len(fr.readlines())
                # if(all_lines > num):
                for line in fr.readlines():
                    #将本人的话显示在右，好友的话显示在左
                    i = i + 1
                    if(i%2 == 1):
                        if (line[0:10] == self.friend):
                            self.textBrowser.setAlignment(QtCore.Qt.AlignLeft)
                        else:
                            self.textBrowser.setAlignment(QtCore.Qt.AlignRight)
                    self.textBrowser.append(line)
                # num = all_lines
                self.cursor = self.textBrowser.textCursor()
                self.textBrowser.moveCursor(self.cursor.End)
                #time.sleep(1)

    def sendmessage(self):
        word = self.lineEdit.text()
        if(word==""):
            QtWidgets.QMessageBox.about(self, "提示", "不能发送空消息！")
        else:
            self.connect.SendMessage(self.usr, self.friend, self.friendIP, word,2)
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










