# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'querydialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Query(object):
    def setupUi(self, Query):
        Query.setObjectName("Query")
        Query.resize(621, 535)
        self.tableWidget = QtWidgets.QTableWidget(Query)
        self.tableWidget.setGeometry(QtCore.QRect(220, 20, 401, 521))
        self.tableWidget.setStyleSheet("background-image: url(:/res/res/verright.jpg)")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.frame = QtWidgets.QFrame(Query)
        self.frame.setGeometry(QtCore.QRect(0, 0, 221, 541))
        self.frame.setStyleSheet("background-image: url(:/res/res/verleft.jpg);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.agreeornot = QtWidgets.QPushButton(self.frame)
        self.agreeornot.setGeometry(QtCore.QRect(10, 10, 93, 28))
        self.agreeornot.setStyleSheet("")
        self.agreeornot.setObjectName("agreeornot")
        self.friendID = QtWidgets.QLabel(self.frame)
        self.friendID.setGeometry(QtCore.QRect(10, 90, 80, 25))
        self.friendID.setObjectName("friendID")
        self.uplist = QtWidgets.QPushButton(self.frame)
        self.uplist.setGeometry(QtCore.QRect(120, 10, 93, 28))
        self.uplist.setObjectName("uplist")
        self.IDline = QtWidgets.QLineEdit(self.frame)
        self.IDline.setGeometry(QtCore.QRect(92, 90, 121, 25))
        self.IDline.setObjectName("IDline")
        self.addfriend = QtWidgets.QPushButton(self.frame)
        self.addfriend.setGeometry(QtCore.QRect(10, 130, 93, 28))
        self.addfriend.setObjectName("addfriend")
        self.chatchoose = QtWidgets.QPushButton(self.frame)
        self.chatchoose.setGeometry(QtCore.QRect(120, 130, 93, 28))
        self.chatchoose.setObjectName("chatchoose")
        self.newfriget = QtWidgets.QLabel(self.frame)
        self.newfriget.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.newfriget.setText("")
        self.newfriget.setObjectName("newfriget")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 190, 161, 131))
        self.label.setObjectName("label")
        self.addgroup = QtWidgets.QPushButton(self.frame)
        self.addgroup.setGeometry(QtCore.QRect(10, 180, 93, 28))
        self.addgroup.setObjectName("addgroup")
        self.groupEdit = QtWidgets.QLineEdit(self.frame)
        self.groupEdit.setGeometry(QtCore.QRect(120, 180, 91, 31))
        self.groupEdit.setObjectName("groupEdit")
        self.frame_2 = QtWidgets.QFrame(Query)
        self.frame_2.setGeometry(QtCore.QRect(220, 0, 401, 21))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.person = QtWidgets.QPushButton(self.frame_2)
        self.person.setGeometry(QtCore.QRect(0, 0, 41, 21))
        self.person.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.person.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/res/person.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.person.setIcon(icon)
        self.person.setObjectName("person")
        self.group = QtWidgets.QPushButton(self.frame_2)
        self.group.setGeometry(QtCore.QRect(349, 0, 51, 21))
        self.group.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.group.setObjectName("group")

        self.retranslateUi(Query)
        QtCore.QMetaObject.connectSlotsByName(Query)

    def retranslateUi(self, Query):
        _translate = QtCore.QCoreApplication.translate
        Query.setWindowTitle(_translate("Query", "Dialog"))
        self.agreeornot.setText(_translate("Query", "新联系人"))
        self.friendID.setText(_translate("Query", "用户昵称："))
        self.uplist.setText(_translate("Query", "刷新列表"))
        self.IDline.setPlaceholderText(_translate("Query", "请输入学号ID"))
        self.addfriend.setText(_translate("Query", "添加好友"))
        self.chatchoose.setText(_translate("Query", "开始聊天"))
        self.label.setText(_translate("Query", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Welcome</span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">CC-Chat</span></p></body></html>"))
        self.addgroup.setText(_translate("Query", "新建群聊"))
        self.groupEdit.setPlaceholderText(_translate("Query", "群聊名称"))
        self.group.setText(_translate("Query", "群聊"))
import myres_rc
