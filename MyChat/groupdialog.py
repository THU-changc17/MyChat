# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_chatDialog(object):
    def setupUi(self, chatDialog):
        chatDialog.setObjectName("chatDialog")
        chatDialog.resize(712, 682)
        self.frame_left = QtWidgets.QFrame(chatDialog)
        self.frame_left.setGeometry(QtCore.QRect(10, 60, 261, 601))
        self.frame_left.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_left)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 241, 301))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.lookstate = QtWidgets.QPushButton(self.frame_left)
        self.lookstate.setGeometry(QtCore.QRect(80, 30, 93, 28))
        self.lookstate.setObjectName("lookstate")
        self.frame_right = QtWidgets.QFrame(chatDialog)
        self.frame_right.setGeometry(QtCore.QRect(290, 60, 421, 611))
        self.frame_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_right.setObjectName("frame_right")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_right)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 391, 341))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_right)
        self.lineEdit.setGeometry(QtCore.QRect(20, 400, 391, 111))
        self.lineEdit.setObjectName("lineEdit")
        self.sendmes = QtWidgets.QPushButton(self.frame_right)
        self.sendmes.setGeometry(QtCore.QRect(170, 540, 93, 28))
        self.sendmes.setObjectName("sendmes")
        self.upfile = QtWidgets.QPushButton(self.frame_right)
        self.upfile.setGeometry(QtCore.QRect(30, 360, 41, 28))
        self.upfile.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/up.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upfile.setIcon(icon)
        self.upfile.setObjectName("upfile")
        self.file = QtWidgets.QPushButton(self.frame_right)
        self.file.setGeometry(QtCore.QRect(80, 360, 41, 28))
        self.file.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/file.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.file.setIcon(icon1)
        self.file.setObjectName("file")
        self.filestate = QtWidgets.QLabel(self.frame_right)
        self.filestate.setGeometry(QtCore.QRect(150, 370, 101, 16))
        self.filestate.setObjectName("filestate")
        self.top_label = QtWidgets.QLabel(chatDialog)
        self.top_label.setGeometry(QtCore.QRect(10, 0, 701, 51))
        self.top_label.setAutoFillBackground(True)
        self.top_label.setText("")
        self.top_label.setObjectName("top_label")

        self.retranslateUi(chatDialog)
        QtCore.QMetaObject.connectSlotsByName(chatDialog)

    def retranslateUi(self, chatDialog):
        _translate = QtCore.QCoreApplication.translate
        chatDialog.setWindowTitle(_translate("chatDialog", "Dialog"))
        self.lookstate.setText(_translate("chatDialog", "刷新状态"))
        self.sendmes.setText(_translate("chatDialog", "发送"))
        self.sendmes.setShortcut(_translate("chatDialog", "Return"))
        self.filestate.setText(_translate("chatDialog", "文件状态"))
