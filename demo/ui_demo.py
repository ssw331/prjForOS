# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pButton_demo_01 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pButton_demo_01.setGeometry(QtCore.QRect(330, 220, 75, 24))
        self.pButton_demo_01.setAutoDefault(False)
        self.pButton_demo_01.setObjectName("pButton_demo_01")
        self.l_demo_01 = QtWidgets.QLabel(parent=self.centralwidget)
        self.l_demo_01.setEnabled(True)
        self.l_demo_01.setGeometry(QtCore.QRect(200, 20, 351, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.l_demo_01.setFont(font)
        self.l_demo_01.setObjectName("l_demo_01")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pButton_demo_01.setText(_translate("MainWindow", "失忆喷雾"))
        self.l_demo_01.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">这是什么？一个按钮，点一下。</span></p></body></html>"))