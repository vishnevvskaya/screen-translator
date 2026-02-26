from PyQt5.QtCore import QThread, pyqtSignal
from paddleocr import PaddleOCR
from pathlib import Path

from .Logger import *

model_dir = Path('./paddle_models')

class ModelLoadedThread(QThread):
    '''Thread for loading the PaddleOCR model'''
    loaded = pyqtSignal(object)

    def __init__(self, lang_value):
        super().__init__()
        self.lang_value = lang_value
    
    def run(self):
        logger.debug(f'Starting PaddleOCR model loading...')
        try:
            model = PaddleOCR(lang=self.lang_value,
                            use_doc_orientation_classify=False,
                            use_doc_unwarping=False,
                            use_textline_orientation=False, 
                            device='gpu',
                            text_detection_model_dir=f'{model_dir}/PP-OCRv5_server_det',
                            text_recognition_model_dir=f'{model_dir}/PP-OCRv5_server_rec')
            logger.info(f'PaddleOCR model for language {self.lang_value} successfully loaded')
            self.loaded.emit(model)
        except Exception as e:
            logger.error(f'Failed to load PaddleOCR model: ', {e})
            self.loaded.emit(None)
        
class RecognitionThread(QThread):
    '''Thread for continuous text recognition and translation'''
    text_translated = pyqtSignal(str)

    def __init__(self, selection, translator, text_recognition, interval):
        super().__init__()
        self.selection = selection
        self.translator = translator
        self.text_recognition = text_recognition
        self.interval = int(float(interval.split()[0])*1000)
        self.flag = True

        logger.info(f'Initializing RecognitionThread with interval: {self.interval} ms')

    def run(self):
        while self.flag:
            try:
                text_recognized = self.text_recognition.get_window_text(self.selection)
                text = self.translator.set_translator(text_recognized)
                self.text_translated.emit(text)
                self.msleep(self.interval)
            except Exception as e:
                logger.error(f'Error in recognition-translation loop: {e}')
                self.msleep(1000)
        logger.info('RecognitionThread stopped')

    def stop(self):
        self.flag = False