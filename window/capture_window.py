from PyQt5 import QtWidgets, QtCore, QtGui

from core.CaptureHandler import CaptureHandler

class CaptureWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(None)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

        self.showFullScreen()
        self.setWindowOpacity(0.4)
        self.setStyleSheet("background-color: #222222;")
        
        self.capture_handler = CaptureHandler(self)