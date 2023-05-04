import PyQt6.QtCore as QtC
import PyQt6.QtWidgets as QtW

import ui_demo as ui
import dialog_01 as dia

class M_Window(QtW.QMainWindow):
    signal = QtC.pyqtSignal(str)  # ?
    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pButton_demo_01.clicked.connect(self.ForClick)  # 只是传了一个函数*名*，而不是函数的结果
        self.signal.connect(self.Signal_rece)

    def ForClick(self):
        self.window = dia.Dialog(self.signal)
        self.window.show()

    def Signal_rece(self, content:str):
        self.ui.l_demo_01.setText(content)
