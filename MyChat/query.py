import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from querydialog import Ui_Query
from chat import chatForm
from group import groupForm
import socket
import threading
from P2Pconnect import P2Pconnect
import time

servername = '166.111.140.57'
serverPort = 8000

class queryForm(QtWidgets.QDialog,Ui_Query):
    def __init__(self,id):
        super(queryForm,self).__init__()
        self.setupUi(self)
        palette = QtGui.QPalette()
        palette.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 255))
        self.setPalette(palette)
        #self.setPalette(palette)
        #self.chatform = 10*[QtWidgets.QDialog()]
        #print(self.chatform)
        self.id = id
        #self.i = 0
        self.usrIP = ''
        self.friendIP = ''
        self.chatform = {}
        self.groupform = {}
        self.exitjudge = {}
        self.newfrilist = []
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setWindowTitle(str(self.id) + "的主页")
        self.setWindowIcon(QtGui.QIcon('res/myico.ico'))
        self.servername = '166.111.140.57'
        self.serverPort = 8000
        self.database = QtSql.QSqlDatabase.addDatabase('QSQLITE','U'+self.id)
        self.database.setDatabaseName('users/data_' + self.id + '.db')
        self.database.open()
        query = QtSql.QSqlQuery(self.database)
        createstr = "create table friendlist (id varchar primary key)"
        # print(createstr)
        query.prepare(createstr)
        query.exec_()
        createstr = "create table grouplist (id varchar primary key)"
        # print(createstr)
        query.prepare(createstr)
        query.exec_()
        try:
            self.clientSocket.connect((self.servername, self.serverPort))
            mysentence = 'q' + self.id
            self.clientSocket.send(mysentence.encode())
            mymes_return = self.clientSocket.recv(2048)
            print(mymes_return)
            self.usrIP = mymes_return.decode()
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "提示", "无法连接服务器！")
        #self.search.clicked.connect(self.search_IP)
        self.chatchoose.clicked.connect(self.startchat)
        #self.lookmes.clicked.connect(self.looknewmes)
        self.person.clicked.connect(self.lookperson)
        self.group.clicked.connect(self.lookgroup)
        self.addfriend.clicked.connect(self.addnewfriend)
        self.connect = P2Pconnect(self.id,self.usrIP)
        self.agreeornot.clicked.connect(self.agreenew)
        self.uplist.clicked.connect(self.loadfriend)
        self.addgroup.clicked.connect(self.addnewgroup)
        self.loadfriend()
        self.agree_Signal.connect(self.agree)
        self.mescall_Signal.connect(self.mescall)
        self.groupmescall_Signal.connect(self.groupmescall)
        #self.filecall_Signal.connect(self.filecall)
        self.frioffline_Signal.connect(self.frioffline)
        self.groupcall_Signal.connect(self.groupcall)
        self.tableWidget.doubleClicked.connect(self.openchat)
        #新建线程监听连接
        self.listenthread = threading.Thread(target = self.connect.Listen)
        #self.listenthread.setDaemon(True)
        self.listenthread.start()
        #self.listening = 1
        #新建线程监听新消息
        self.newmeslisten = threading.Thread(target = self.getnewmes)
        #self.listenthread.setDaemon(True)
        self.newmeslisten.start()
        self.getnew = threading.Thread(target = self.getnewstate)
        self.getnew.start()
        self.newstate_Signal.connect(self.newstatechange)
#主页用到的监听信号
    agree_Signal = QtCore.pyqtSignal(str)
    mescall_Signal = QtCore.pyqtSignal(int)
    frioffline_Signal = QtCore.pyqtSignal(str)
    groupcall_Signal = QtCore.pyqtSignal(str)
    groupmescall_Signal = QtCore.pyqtSignal(int)
    newstate_Signal = QtCore.pyqtSignal(list,list)
    #filecall_Signal = QtCore.pyqtSignal(int)

    def closeEvent(self,event):
        idlist = []
        statelist = []
        query = QtSql.QSqlQuery(self.database)
        query.prepare('select id from friendlist')
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                idlist.append(query.value(0))
        for person in idlist:
            sentence = 'q' + person
            self.clientSocket.send(sentence.encode())
            mes_return = self.clientSocket.recv(2048).decode()
            statelist.append(mes_return)
        reply =QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出账号?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for i in range(len(idlist)):
                if(statelist[i]!="n"):
                    print(idlist[i])
                    print(statelist[i])
                    self.connect.SendMessage(self.id, idlist[i], statelist[i], "离线", 3)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((servername, serverPort))
            sentence = 'logout' + self.id
            clientSocket.send(sentence.encode())
            mes_return = clientSocket.recv(2048)
            clientSocket.close()
            if (mes_return.decode() != "loo"):
                QtWidgets.QMessageBox.about(self, "提示", "服务器故障，无法下线")
            self.database.close()
            event.accept()
            os._exit(0)
        else:
            event.ignore()
#动态刷新
    def newstatechange(self,rev_idlist,rev_statelist):
        i = j = 0
        if(self.tableWidget.columnCount()==4):
            self.tableWidget.setRowCount(len(rev_idlist))
            for person in rev_idlist:
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(person))
                j = j + 1
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(rev_statelist[i]))
                j = j + 2
                if(self.tableWidget.item(i,j)==None):
                    check = QtWidgets.QTableWidgetItem()
                    check.setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
                    self.tableWidget.setItem(i, j, check)  # 在(x,y)添加checkBox
                i = i + 1
                j = 0

    def getnewstate(self):
        while(1):
            idlist = []
            statelist = []
            query = QtSql.QSqlQuery(self.database)
            query.prepare('select id from friendlist')
            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    idlist.append(query.value(0))
            # query.finish()
            for person in idlist:
                sentence = 'q' + person
                self.clientSocket.send(sentence.encode())
                mes_return = self.clientSocket.recv(2048)
                if (mes_return.decode() == 'n'):
                    statelist.append("离线")
                else:
                    statelist.append("在线")
            self.newstate_Signal.emit(idlist, statelist)
            time.sleep(3)

    def getnewmes(self):
        while True:
            if(self.connect.newmessage == 1):
                rev_wordlist = self.connect.rev_word.split('#')
                friend = rev_wordlist[0]
                #如果从未联系过好友，或之前的界面关闭，发出新消息提示
                if(rev_wordlist[3] == str(0)):
                    self.newfriget.setText(rev_wordlist[2])
                    self.newfrilist.append(friend)
                elif(rev_wordlist[3] == str(1)):
                    if(rev_wordlist[2]=="同意好友申请!"):
                        #database = QtSql.QSqlDatabase.addDatabase('QSQLITE','U'+self.id)
                        #self.database.open()
                        query = QtSql.QSqlQuery(self.database)
                        insertstr = "insert into friendlist (id) values(?)"
                        #print(insertstr)
                        query.prepare(insertstr)
                        query.addBindValue(friend)
                        query.exec_()
                        #query.finish()
                        self.agree_Signal.emit("1"+friend)
                    else:
                        self.agree_Signal.emit("0"+friend)
                elif (rev_wordlist[3] == str(2)):
                    if (friend not in self.chatform or self.exitjudge[friend] == 1):
                        # self.newmes.setText("来自" + self.connect.rev_word[0:10] + "的新消息")
                        num = self.tableWidget.rowCount()
                        # print(num)
                        for i in range(0, num):
                            if (self.tableWidget.item(i, 0).text() == self.connect.rev_word[0:10]):  # and self.connect.newfile==0):
                                self.mescall_Signal.emit(i)
                                # print(i)
                elif(rev_wordlist[3] == str(3)):
                    if(self.exitjudge[friend] == 0):
                        self.frioffline_Signal.emit(friend)
                elif(rev_wordlist[3] == str(5)):
                    group_id = self.connect.rev_grouplist[-1]
                    self.groupcall_Signal.emit(group_id)
                    query = QtSql.QSqlQuery(self.database)
                    insertstr = "insert into grouplist (id) values(?)"
                    query.prepare(insertstr)
                    query.addBindValue(group_id)
                    query.exec_()
                    createstr = "create table " + group_id + " " + "(id varchar primary key)"
                    # print(createstr)
                    query.prepare(createstr)
                    query.exec_()
                    leng = len(self.connect.rev_grouplist)
                    for friend in self.connect.rev_grouplist[0:leng-1]:
                        # 群聊好友按照“-”区分
                        insertstr = "insert into " + group_id + "(id) values(?)"
                        query.prepare(insertstr)
                        query.addBindValue(friend)
                        query.exec_()
                elif (rev_wordlist[3] == str(6)):
                    groupinfo = self.connect.group_word[1]
                    if (groupinfo not in self.groupform or self.exitjudge[groupinfo] == 1):
                        # self.newmes.setText("来自" + self.connect.rev_word[0:10] + "的新消息")
                        num = self.tableWidget.rowCount()
                        # print(num)
                        for i in range(0, num):
                            if (self.tableWidget.item(i, 0).text() == groupinfo):  # and self.connect.newfile==0):
                                self.groupmescall_Signal.emit(i)
                time.sleep(0.1)

    def agree(self,friendret):
        if(friendret[0]=="1"):
            QtWidgets.QMessageBox.about(self, "提示", friendret[1:] + "已同意您的好友申请！")
        else:
            QtWidgets.QMessageBox.about(self, "提示", friendret[1:] + "未同意您的好友申请！")

    def mescall(self,revint):
        label_pic = QtWidgets.QLabel()
        label_pic.setPixmap(QtGui.QPixmap("res/chat.jpg"))
        self.tableWidget.setCellWidget(revint,2,label_pic)
#消息提醒图标
    def groupmescall(self,revint):
        label_pic = QtWidgets.QLabel()
        label_pic.setPixmap(QtGui.QPixmap("res/chat.jpg"))
        self.tableWidget.setCellWidget(revint,1,label_pic)
#好友下线处理
    def frioffline(self,friend):
        QtWidgets.QMessageBox.about(self, "提示", friend+"已下线！")
        self.chatform[friend].lineEdit.setText("对方已下线！")
        self.chatform[friend].lineEdit.setReadOnly(True)
#群聊添加提醒
    def groupcall(self,group):
        QtWidgets.QMessageBox.about(self, "提示", "您已被添加到群聊" +group)

    def newchatform(self,friend,friendIP):
        # 如果从未打开过此好友界面，则新建
        if(friend not in self.chatform):
            self.chatform[friend] = chatForm(self.connect,self.id, friend, self.usrIP, friendIP)
        self.exitjudge[friend] = 0
        #接收子界面关闭的信号
        self.chatform[friend].my_Signal.connect(lambda:self.form_exit(friend))
        self.chatform[friend].lineEdit.setText("")
        self.chatform[friend].lineEdit.setReadOnly(False)
        self.chatform[friend].show()
        #self.chatform[friend].exec_()

    def newgroupform(self,group,group_friend):
        if (group not in self.groupform):
            self.groupform[group] = groupForm(self.connect,self.id,group,group_friend)
        self.exitjudge[group] = 0
        # 接收子界面关闭的信号
        self.groupform[group].group_Signal.connect(lambda: self.form_exit(group))
        #self.chatform[group].lineEdit.setText("")
        #self.chatform[group].lineEdit.setReadOnly(False)
        self.groupform[group].show()

    #表示子聊天及群聊界面已经关闭
    def form_exit(self,friend):
        self.exitjudge[friend] = 1

    def startchat(self):
        friend = self.IDline.text()
        idlist = []
        judge = 0
        query = QtSql.QSqlQuery(self.database)
        query.prepare('select id from friendlist')
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                idlist.append(query.value(0))
        for person in idlist:
            if(person==friend):
                judge = 1
        if(judge == 0):
            QtWidgets.QMessageBox.about(self, "提示", "此用户不是您的好友,无法聊天")
        else:
            sentence = 'q' + friend
            self.clientSocket.send(sentence.encode())
            frimes_return = self.clientSocket.recv(2048).decode()
            if (frimes_return != "n"):
                self.newchatform(friend, frimes_return)
            else:
                QtWidgets.QMessageBox.about(self, "提示", "此好友不在线,无法聊天")
        #chatform.show()
        #self.chatform[self.i] = chatForm(usr,friend,self.usrIP,self.friendIP)
        #self.chatform[self.i].show()
        #self.i += 1

    def openchat(self,index):
        if(self.tableWidget.columnCount()==4):
            currfriend = self.tableWidget.item(index.row(), 0).text()
            sentence = 'q' + currfriend
            self.clientSocket.send(sentence.encode())
            frimes_return = self.clientSocket.recv(2048).decode()
            if (frimes_return != "n"):
                self.tableWidget.removeCellWidget(index.row(), 2)
                self.newchatform(currfriend, frimes_return)
            else:
                QtWidgets.QMessageBox.about(self, "提示", "此好友不在线,无法聊天")
        else:
            currgroup = self.tableWidget.item(index.row(), 0).text()
            groupfrilist = []
            query = QtSql.QSqlQuery(self.database)
            query.prepare('select id from ' + currgroup)
            if not query.exec_():
                query.lastError()
                #print("no open")
            else:
                while query.next():
                    groupfrilist.append(query.value(0))
                self.tableWidget.removeCellWidget(index.row(), 1)
                self.newgroupform(currgroup,groupfrilist)

    def loadfriend(self):
        #self.database.open()
        try:
            idlist = []
            statelist = []
            query = QtSql.QSqlQuery(self.database)
            query.prepare('select id from friendlist')
            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    idlist.append(query.value(0))
            #query.finish()
            for person in idlist:
                sentence = 'q' + person
                self.clientSocket.send(sentence.encode())
                mes_return = self.clientSocket.recv(2048)
                if (mes_return.decode() == 'n'):
                    statelist.append("离线")
                else:
                    statelist.append("在线")
                self.exitjudge[person] = 1

            self.tableWidget.setFrameShape(0)
            #self.tableWidget.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tableWidget.setRowCount(len(idlist))
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(['好友', '在线状态','消息提醒','群聊添加'])
            self.tableWidget.verticalHeader().setHidden(True)
            i = j = 0
            for person in idlist:
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(person))
                j = j + 1
                self.tableWidget.removeCellWidget(i, j)
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(statelist[i]))
                j = j + 2
                check = QtWidgets.QTableWidgetItem()
                check.setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
                self.tableWidget.setItem(i, j, check)  # 在(x,y)添加checkBox
                i = i + 1
                j = 0
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "提示", "连接数据库错误")

    def lookperson(self):
        try:
            idlist = []
            statelist = []
            query = QtSql.QSqlQuery(self.database)
            query.prepare('select id from friendlist')
            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    idlist.append(query.value(0))
            #query.finish()
            for person in idlist:
                sentence = 'q' + person
                self.clientSocket.send(sentence.encode())
                mes_return = self.clientSocket.recv(2048)
                if (mes_return.decode() == 'n'):
                    statelist.append("离线")
                else:
                    statelist.append("在线")
                self.exitjudge[person] = 1

            self.tableWidget.setFrameShape(0)
            #self.tableWidget.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tableWidget.setRowCount(len(idlist))
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(['好友', '在线状态','消息提醒','群聊添加'])
            self.tableWidget.verticalHeader().setHidden(True)
            i = j = 0
            for person in idlist:
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(person))
                j = j + 1
                self.tableWidget.removeCellWidget(i, j)
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(statelist[i]))
                j = j + 2
                check = QtWidgets.QTableWidgetItem()
                check.setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
                self.tableWidget.setItem(i, j, check)  # 在(x,y)添加checkBox
                i = i + 1
                j = 0
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "提示", "连接数据库错误")

    def lookgroup(self):
        try:
            idlist = []
            #statelist = []
            query = QtSql.QSqlQuery(self.database)
            query.prepare('select id from grouplist')
            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    idlist.append(query.value(0))
            self.tableWidget.setFrameShape(0)
            #self.tableWidget.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tableWidget.setRowCount(len(idlist))
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(['我所在的群聊','消息提醒'])
            self.tableWidget.verticalHeader().setHidden(True)
            i = 0
            for group in idlist:
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(group))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(""))
                i = i + 1
        except Exception as e:
            QtWidgets.QMessageBox.about(self, "提示", "连接数据库错误")
#添加好友
    def addnewfriend(self):
        #self.database.open()
        sentence = 'q' + self.IDline.text()
        self.clientSocket.send(sentence.encode())
        mes_return = self.clientSocket.recv(2048)
        if (mes_return.decode()[0].isalpha() == True):
            QtWidgets.QMessageBox.about(self, "提示", "您查找的用户不在线！")
        else:
            judge = 0
            num = self.tableWidget.rowCount()
            for i in range(0, num):
                if (self.tableWidget.item(i, 0).text() == self.IDline.text()):
                    QtWidgets.QMessageBox.about(self, "提示", "该用户是您的好友！")
                    judge = 1
            if(judge == 0):
                self.connect.SendMessage(self.id,self.IDline.text(),mes_return,"新的好友申请!",0)
        #query.finish()
#处理好友添加信息
    def agreenew(self):
        if(self.newfriget.text()!=""):
            for friend in self.newfrilist:
                reply = QtWidgets.QMessageBox.question(self,
                                                       '新好友'+friend,
                                                       "是否添加好友?",
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    #database = QtSql.QSqlDatabase.addDatabase('QSQLITE','U'+self.id)
                    #self.database.open()
                    query = QtSql.QSqlQuery(self.database)
                    insertstr = "insert into friendlist (id) values(?)"
                    #print(insertstr)
                    query.prepare(insertstr)
                    query.addBindValue(friend)
                    #print(friend)
                    query.exec_()
                    QtWidgets.QMessageBox.about(self, "提示", "添加好友成功啦")
                    #query.finish()
                    sentence = 'q' + friend
                    self.clientSocket.send(sentence.encode())
                    frimes_return = self.clientSocket.recv(2048).decode()
                    self.connect.SendMessage(self.id,friend, frimes_return, "同意好友申请!", 1)
                else:
                    sentence = 'q' + friend
                    self.clientSocket.send(sentence.encode())
                    frimes_return = self.clientSocket.recv(2048).decode()
                    self.connect.SendMessage(self.id, friend, frimes_return, "未同意好友申请!", 1)
            self.newfriget.setText("")
            self.newfrilist = []
#新建群聊
    def addnewgroup(self):
        group_friend = []
        for i in range(self.tableWidget.rowCount()):
            if(self.tableWidget.item(i,3).checkState()):
                group_friend.append(self.tableWidget.item(i,0).text())
        group_friend.append(self.id)
        group_id = self.groupEdit.text() + self.id  #群聊名称为群聊ID+用户ID
        judge_group_same = 0 #判断群聊名称是否重复
        query = QtSql.QSqlQuery(self.database)
        query.prepare('select id from grouplist')
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                if(query.value(0)==group_id):
                    judge_group_same = 1
        if(judge_group_same == 1):
            QtWidgets.QMessageBox.about(self, "提示", "群聊ID已存在！")
        elif(group_id == self.id):
            QtWidgets.QMessageBox.about(self, "提示", "群聊ID不可为空！")
        elif(len(group_friend) < 3):
            QtWidgets.QMessageBox.about(self, "提示", "群组至少为3人！")
        else:
            jud = 0
            for friend in group_friend:
                sentence = 'q' + friend
                self.clientSocket.send(sentence.encode())
                frimes_return = self.clientSocket.recv(2048).decode()
                if (frimes_return == "n"):
                    jud = 1
            #查看添加群聊的好友是否均在线
            if(jud==0):
                query = QtSql.QSqlQuery(self.database)
                insertstr = "insert into grouplist (id) values(?)"  #群聊名称数据库
                # print(insertstr)
                query.prepare(insertstr)
                query.addBindValue(group_id)
                query.exec_()
                createstr = "create table " + group_id + " " + "(id varchar primary key)" #群聊好友信息数据库
                # print(createstr)
                query.prepare(createstr)
                query.exec_()
                groupword = group_id
                for friend in group_friend:
                    # 群聊好友按照“-”区分
                    groupword = str(friend) + "-" + groupword
                    insertstr = "insert into " + group_id + "(id) values(?)"
                    # print(insertstr)
                    query.prepare(insertstr)
                    query.addBindValue(friend)
                    # print(friend)
                    query.exec_()
                group_friend.remove(self.id)
                # group_friend.append(self.id)
                for friend in group_friend:
                    sentence = 'q' + friend
                    self.clientSocket.send(sentence.encode())
                    frimes_return = self.clientSocket.recv(2048).decode()
                    self.connect.SendMessage(self.id, friend, frimes_return, groupword, 5)
                QtWidgets.QMessageBox.about(self, "提示", "群聊创建成功！")
            else:
                QtWidgets.QMessageBox.about(self, "提示", "选择的成员有人不在线！")










