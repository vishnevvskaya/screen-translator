from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from window.main_window import MainWindow

if __name__ == "__main__":
    import ctypes
    import sys

    if sys.platform == "win32":
        myappid = 'screen.translator.app.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 