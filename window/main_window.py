from PyQt5 import QtWidgets

from window.interface import Ui_MainWindow
from core.ActionHandler import ActionHandler

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.action_handler = ActionHandler(self.ui, self)