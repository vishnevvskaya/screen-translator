from PyQt5 import QtWidgets, QtCore, QtGui

from core.TranslationHandler import TranslationHandler

class TranslationWindow(QtWidgets.QWidget):
    def __init__(self, selection, settings):
        super().__init__(None)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)
        
        self.resize(1000, 150)
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height() + 300) // 2
        self.move(x, y)
        self.setMinimumSize(1000, 150)

        self.setWindowOpacity(0.85)
        self.setStyleSheet("background-color: #222222;")

        self.setup_ui()
        self.translation_handler = TranslationHandler(self, selection, settings)
    
    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        top_panel = QtWidgets.QWidget()
        top_layout = QtWidgets.QHBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addStretch()
        main_layout.addWidget(top_panel)

        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.setText('×')
        self.close_button.setStyleSheet("background-color: transparent; border: none; color: #FFFFFF;")
        self.close_button.resize(30, 30)
        top_layout.addWidget(self.close_button)

        self.text_area = QtWidgets.QTextEdit()
        self.text_area.viewport().setCursor(QtCore.Qt.ArrowCursor)
        self.text_area.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.text_area.setStyleSheet("border: none; color: #FFFFFF; font-family: 'Cascadia Mono Light'; font-size: 15px;")
        main_layout.addWidget(self.text_area)

        bottom_panel = QtWidgets.QWidget()
        bottom_layout = QtWidgets.QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()
        main_layout.addWidget(bottom_panel)

        self.resize_label = QtWidgets.QLabel(self)
        self.resize_label.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
        self.resize_label.setText('...')
        self.resize_label.setStyleSheet("background-color: transparent; border: none; color: #FFFFFF;")
        bottom_layout.addWidget(self.resize_label)