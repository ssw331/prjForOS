# Form implementation generated from reading ui file 'demo_sub.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_demo_01(object):
    def setupUi(self, Dialog_demo_01):
        Dialog_demo_01.setObjectName("Dialog_demo_01")
        Dialog_demo_01.resize(400, 300)
        self.buttonBox_demo_01 = QtWidgets.QDialogButtonBox(parent=Dialog_demo_01)
        self.buttonBox_demo_01.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox_demo_01.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox_demo_01.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox_demo_01.setObjectName("buttonBox_demo_01")
        self.l_demosub_01 = QtWidgets.QLabel(parent=Dialog_demo_01)
        self.l_demosub_01.setGeometry(QtCore.QRect(130, 80, 141, 31))
        self.l_demosub_01.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l_demosub_01.setObjectName("l_demosub_01")
        self.textEdit = QtWidgets.QTextEdit(parent=Dialog_demo_01)
        self.textEdit.setGeometry(QtCore.QRect(100, 130, 201, 71))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog_demo_01)
        self.buttonBox_demo_01.accepted.connect(Dialog_demo_01.accept)  # type: ignore
        self.buttonBox_demo_01.rejected.connect(Dialog_demo_01.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_demo_01)

    def retranslateUi(self, Dialog_demo_01):
        _translate = QtCore.QCoreApplication.translate
        Dialog_demo_01.setWindowTitle(_translate("Dialog_demo_01", "Dialog"))
        self.l_demosub_01.setText(_translate("Dialog_demo_01", "失忆喷雾没了~~~"))
