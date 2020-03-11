import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtWidgets,QtGui,QtCore
from filedialog import Ui_filedlg
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
import os
import sys

class fileForm(QtWidgets.QWidget,Ui_filedlg):
    def __init__(self,usr,friend):
        super(fileForm,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("文件页")
        self.setWindowIcon(QtGui.QIcon('res/myico.ico'))
        palette = QtGui.QPalette()
        pix = QtGui.QPixmap("res/tim.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)
        self.usr = usr
        self.friend = friend
        self.filelist = []
        #self.dirlist = []
        self.file_dir = 'users/' + usr + '/' + 'files/' + friend
        len = 0
        for root, dirs, files in os.walk(self.file_dir, topdown=False):
            for filename in files:
                self.filelist.append(filename)
                len += 1
        print(self.filelist)
        #print(self.root)
        #print(self.dirlist)
        self.tableWidget.setFrameShape(0)
        # self.tableWidget.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setRowCount(len)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(['文件名'])
        self.tableWidget.verticalHeader().setHidden(True)
        i = 0
        for name in self.filelist:
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            #print(name)
            i += 1
        self.tableWidget.doubleClicked.connect(self.openfile)

    def openfile(self,index):
        currname = self.tableWidget.item(index.row(), 0).text()
        print(currname)
        os.startfile(os.path.abspath(".") + '/' + self.file_dir + '/' + currname)

