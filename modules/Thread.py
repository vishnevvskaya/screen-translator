from PyQt5.QtCore import QThread, pyqtSignal
from paddleocr import PaddleOCR

model_dir = r"./paddle_models" 

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
    text_recognized = pyqtSignal(str)

    def __init__(self, selection, text_recognition):
        super().__init__()
        self.selection = selection
        self.text_recognition = text_recognition
        self.flag = True

    def run(self):
        while self.flag:
            text = self.text_recognition.get_window_text(self.selection)
            self.msleep(100)
        self.text_recognized.emit(text)

    def stop(self):
        self.flag = False