import PyQt6.QtWidgets as QtW

import ui_demo_sub

class Dialog(QtW.QDialog):
    def __init__(self,signal):
        super().__init__()
        self.ui = ui_demo_sub.Ui_Dialog_demo_01()
        self.ui.setupUi(self)
        self.signal = signal

    def accept(self) -> None:
        content = self.ui.textEdit.toPlainText()
        self.signal.emit(content)
        super().accept()  # 用以调用原本的accept


