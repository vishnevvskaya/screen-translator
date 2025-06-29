from PyQt5 import QtCore, QtWidgets, QtGui

from window.translation_window import TranslationWindow

class CaptureHandler(QtCore.QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.translation_window = None

        self.selection = None
        self.drawing = False

        self.window.mousePressEvent = lambda e: self.setup_events('press', e)
        self.window.mouseMoveEvent = lambda e: self.setup_events('move', e)
        self.window.mouseReleaseEvent = lambda e: self.setup_events('release', e)
        self.window.paintEvent = self.paint_event

        self.setup_hotkey()
    
    def setup_hotkey(self):
        '''Setting up hot keys'''
        self.hotkey = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.window)
        self.hotkey.activated.connect(self.window.close)
    
    def setup_events(self, event_type, event):
        '''Connecting signals to mouse events'''
        if event.button() == QtCore.Qt.LeftButton or event_type == 'move':
            if event_type == 'press':
                self.drawing = True
                self.selection = [event.pos(), event.pos()]
            elif event_type == 'move' and self.drawing:
                self.selection[1] = event.pos()
            elif event_type == 'release' and self.drawing:
                self.drawing = False
                print(QtCore.QRect(*self.selection).normalized())
                self.window.close()

                if self.translation_window is not None:
                    self.translation_window.deleteLater()

                self.translation_window = TranslationWindow(self.selection)
                self.translation_window.showMinimized()
                self.translation_window.show()
            self.window.update()
    
    def paint_event(self, event):
        '''Drawing the selected area'''
        if self.drawing and self.selection:
            painter = QtGui.QPainter(self.window)
            selection_rect = QtCore.QRect(*self.selection).normalized()
            painter.setPen(QtGui.QPen(QtCore.Qt.blue, 1))
            painter.drawRect(selection_rect)
            painter.fillRect(selection_rect, QtCore.Qt.NoBrush)
            painter.end()