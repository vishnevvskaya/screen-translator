from PyQt5.QtCore import QThread, pyqtSignal
from paddleocr import PaddleOCR
from pathlib import Path

model_dir = Path('./paddle_models')

class ModelLoadedThread(QThread):
    loaded = pyqtSignal(object)

    def __init__(self, lang_value):
        super().__init__()
        self.lang_value = lang_value
    
    def run(self):
        model = PaddleOCR(lang=self.lang_value,
                        use_doc_orientation_classify=False,
                        use_doc_unwarping=False,
                        use_textline_orientation=False, 
                        device='gpu',
                        text_detection_model_dir=f'{model_dir}/det',
                        text_recognition_model_dir=f'{model_dir}/rec')
        self.loaded.emit(model)
        
class RecognitionThread(QThread):
    text_translated = pyqtSignal(str)

    def __init__(self, selection, translator, text_recognition, interval):
        super().__init__()
        self.selection = selection
        self.translator = translator
        self.text_recognition = text_recognition
        self.interval = int(float(interval.split()[0])*1000)
        self.flag = True

    def run(self):
        while self.flag:
            text_recognized = self.text_recognition.get_window_text(self.selection)
            text = self.translator.set_translator(text_recognized)
            self.text_translated.emit(text)
            self.msleep(self.interval)

    def stop(self):
        self.flag = False