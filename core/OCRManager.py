from PyQt5 import QtCore

from modules import *

class OCRManager:
    def __init__(self):
        self.recognition_thread = None
        self.recognition_timer = QtCore.QTimer()
        self.recognition_timer.timeout.connect(self.recognize_text)
    
    def setup(self):
        '''Setting up periodic recognition'''
        interval = int(float(self.settings['refresh_screen'].split()[0])*1000)
        self.recognition_timer.start(interval)
    
    def recognize_text(self):
        '''Performing text recognition'''
        if self.recognition_thread and self.recognition_thread.isRunning():
            self.recognition_thread.stop()
        
        text_recognition = TextRecognition(self.settings['from_lang'])
        self.recognition_thread = RecognitionThread(self.selection, text_recognition)
        self.recognition_thread.text_recognized.connect(lambda text: (self.window.text_area.setText(text), print(text)))
        self.recognition_thread.start()
    
    def close(self):
        '''Resource cleaning'''
        self.recognition_timer.stop()
        if self.recognition_thread:
            self.recognition_thread.stop()
        self.window.close()