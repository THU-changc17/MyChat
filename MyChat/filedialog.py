# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filedialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_filedlg(object):
    def setupUi(self, filedlg):
        filedlg.setObjectName("filedlg")
        filedlg.resize(400, 300)
        self.tableWidget = QtWidgets.QTableWidget(filedlg)
        self.tableWidget.setGeometry(QtCore.QRect(70, 50, 261, 221))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(filedlg)
        self.label.setGeometry(QtCore.QRect(90, 20, 211, 16))
        self.label.setObjectName("label")

        self.retranslateUi(filedlg)
        QtCore.QMetaObject.connectSlotsByName(filedlg)

    def retranslateUi(self, filedlg):
        _translate = QtCore.QCoreApplication.translate
        filedlg.setWindowTitle(_translate("filedlg", "Dialog"))
        self.label.setText(_translate("filedlg", "双击文件名使用默认应用打开！"))
