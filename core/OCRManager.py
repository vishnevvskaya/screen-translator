from PyQt5 import QtCore

from modules import *

class OCRManager:
    def __init__(self):
        self.recognition_thread = None
    
    def setup(self):
        '''Setting up periodic recognition'''
        if self.recognition_thread:
            self.recognition_thread.stop()
        self.start_recognition()
    
    def start_recognition(self):
        '''Performing text recognition'''
        if self.recognition_thread and self.recognition_thread.isRunning():
            return
        
        text_recognition = TextRecognition(self.settings['from_lang'])
        translator = Translator(self.settings['translator'], int(self.settings['from_lang']), int(self.settings['to_lang']))

        self.recognition_thread = RecognitionThread(self.selection, translator, text_recognition, self.settings['refresh_screen'])
        self.recognition_thread.text_translated.connect(lambda text: self.window.text_area.setText(text))
        self.recognition_thread.start()

    def close(self):
        '''Resource cleaning'''
        if self.recognition_thread:
            self.recognition_thread.stop()
            self.recognition_thread = None
        self.window.close()