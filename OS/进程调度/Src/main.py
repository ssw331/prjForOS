import PyQt6.QtWidgets as QtW
import sys

import Main_Window

app = QtW.QApplication(sys.argv)
window = Main_Window.M_Window()
window.show()
sys.exit(app.exec())
