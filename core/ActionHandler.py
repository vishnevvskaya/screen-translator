from PyQt5 import QtCore, QtWidgets, QtGui

from modules.Utils import Utils
from window.capture_window import CaptureWindow

class ActionHandler(QtCore.QObject):
    def __init__(self, ui, window):
        super().__init__()
        self.ui = ui
        self.window = window

        self.current_lang = 'en'
        self.capture_window = None
        self.translator = QtCore.QTranslator()

        self.setup_hotkeys()
        self.setup_connections()
    
    def setup_connections(self):
        '''Connecting signals to slots'''
        self.ui.switchlangButton.clicked.connect(self.swap_languages)
        self.ui.enButton.clicked.connect(lambda: self.change_interface_languages('en'))
        self.ui.ruButton.clicked.connect(lambda: self.change_interface_languages('ru'))
        self.ui.resetButton.clicked.connect(self.reset_settings)
    
    def setup_hotkeys(self):
        '''Setting up hot keys'''
        self.hotkey = QtWidgets.QShortcut(QtGui.QKeySequence("F12"), self.window)
        self.hotkey.activated.connect(self.show_capture_window)

    def swap_languages(self):
        '''Swaps the source and target languages'''
        from_lang = self.ui.fromlangComboBox.currentText()
        to_lang = self.ui.tolangComboBox.currentText()

        self.ui.fromlangComboBox.setCurrentText(to_lang)
        self.ui.tolangComboBox.setCurrentText(from_lang)

    def change_interface_languages(self, lang):
        '''Changes the application interface language'''
        app = QtWidgets.QApplication.instance()

        if lang == 'ru':
            if self.translator.load('./assets/translations_ru.qm'):
                app.installTranslator(self.translator)
                lang_list = list(Utils.get_ru_languages().keys())

                self.ui.screenrefreshComboBox.clear()
                for x in (0.4 + 0.2*i for i in range(24) if 0.1 + 0.2*i <= 5.0):
                    self.ui.screenrefreshComboBox.addItem(f"{x:.1f} с")
        else:
            app.removeTranslator(self.translator)
            lang_list = list(Utils.get_en_languages().keys())

            self.ui.screenrefreshComboBox.clear()
            for x in (0.4 + 0.2*i for i in range(24) if 0.1 + 0.2*i <= 5.0):
                self.ui.screenrefreshComboBox.addItem(f"{x:.1f} sec")
    
        self.ui.fromlangComboBox.clear()
        self.ui.tolangComboBox.clear()
        for lang in lang_list:
            self.ui.fromlangComboBox.addItem(lang)
            self.ui.tolangComboBox.addItem(lang)
        self.ui.fromlangComboBox.setCurrentIndex(3)
        self.ui.tolangComboBox.setCurrentIndex(12)

        self.ui.retranslateUi(self.window)

    def reset_settings(self):
        '''Reset current settings'''
        self.ui.fromlangComboBox.setCurrentIndex(3)
        self.ui.tolangComboBox.setCurrentIndex(12)
        self.ui.translatorComboBox.setCurrentIndex(0)
        self.ui.screenrefreshComboBox.setCurrentIndex(0)
    
    def show_capture_window(self):
        '''Shows the screen capture window'''
        current_settings = {
            'from_lang': self.ui.fromlangComboBox.currentIndex(),
            'to_lang': self.ui.tolangComboBox.currentText(),
            'translator': self.ui.translatorComboBox.currentText(),
            'refresh_screen': self.ui.screenrefreshComboBox.currentText(),
        }

        if hasattr(self, 'capture_window') and self.capture_window is not None:
            self.capture_window.close()
            self.capture_window.deleteLater()

        self.capture_window = CaptureWindow(current_settings)

        self.window.showMinimized()
        self.capture_window.show()
        self.capture_window.activateWindow()
        self.capture_window.raise_()