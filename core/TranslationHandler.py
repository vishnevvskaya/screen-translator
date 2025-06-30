from PyQt5 import QtCore

from core.OCRManager import OCRManager
from modules import *

class TranslationHandler(QtCore.QObject):
    def __init__(self, window, selection, settings):
        super().__init__()
        self.window = window

        self.dragging = False
        self.resizing = False

        self.ocr_manager = OCRManager()
        self.ocr_manager.window = window
        self.ocr_manager.selection = selection
        self.ocr_manager.settings = settings

        self.window.mousePressEvent = lambda e: self.setup_events('press', e)
        self.window.mouseMoveEvent = lambda e: self.setup_events('move', e)
        self.window.mouseReleaseEvent = lambda e: self.setup_events('release', e)

        self.setup_connections()
        self.ocr_manager.setup()

    def setup_connections(self):
        '''Connecting signals to slots'''
        self.window.close_button.clicked.connect(self.ocr_manager.close)

    def setup_events(self, event_type, event):
        '''Connecting signals to mouse events'''
        if event.button() == QtCore.Qt.LeftButton and event_type == 'press':
            if self.window.resize_label.rect().contains(self.window.resize_label.mapFrom(self.window, event.pos())):
                self.resizing = True
                self.resize_start_pos = event.globalPos()
                self.resize_start_geometry = self.window.geometry()
            else:
                self.dragging = True
                self.drag_start = event.globalPos() - self.window.pos()
        elif event_type == 'move':
            if self.dragging:
                self.window.move(event.globalPos() - self.drag_start)
            elif self.resizing:
                delta = event.globalPos() - self.resize_start_pos
                new_w = self.resize_start_geometry.width() + delta.x()
                new_h = self.resize_start_geometry.height() + delta.y()
                self.window.setGeometry(self.resize_start_geometry.x(), self.resize_start_geometry.y(), new_w, new_h)
        elif event_type == 'release':
            self.dragging = False
            self.resizing = False