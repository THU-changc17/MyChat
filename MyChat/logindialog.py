# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logindialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(636, 397)
        self.username = QtWidgets.QLabel(login)
        self.username.setGeometry(QtCore.QRect(190, 180, 50, 50))
        self.username.setObjectName("username")
        self.password = QtWidgets.QLabel(login)
        self.password.setGeometry(QtCore.QRect(200, 240, 41, 50))
        self.password.setObjectName("password")
        self.usrline = QtWidgets.QLineEdit(login)
        self.usrline.setGeometry(QtCore.QRect(250, 195, 141, 21))
        self.usrline.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.usrline.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.usrline.setObjectName("usrline")
        self.pasdline = QtWidgets.QLineEdit(login)
        self.pasdline.setGeometry(QtCore.QRect(250, 255, 141, 21))
        self.pasdline.setMaxLength(32768)
        self.pasdline.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pasdline.setObjectName("pasdline")
        self.enter = QtWidgets.QPushButton(login)
        self.enter.setGeometry(QtCore.QRect(260, 330, 93, 28))
        self.enter.setAutoDefault(True)
        self.enter.setObjectName("enter")
        self.photolabel = QtWidgets.QLabel(login)
        self.photolabel.setGeometry(QtCore.QRect(-10, -5, 651, 171))
        self.photolabel.setAutoFillBackground(True)
        self.photolabel.setText("")
        self.photolabel.setObjectName("photolabel")
        self.checkBox = QtWidgets.QCheckBox(login)
        self.checkBox.setGeometry(QtCore.QRect(260, 300, 91, 19))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Form"))
        self.username.setText(_translate("login", "用户名:"))
        self.password.setText(_translate("login", "密码："))
        self.usrline.setPlaceholderText(_translate("login", "请输入用户名"))
        self.pasdline.setPlaceholderText(_translate("login", "请输入密码"))
        self.enter.setText(_translate("login", "登录"))
        self.enter.setShortcut(_translate("login", "Return"))
        self.checkBox.setText(_translate("login", "记住密码"))
