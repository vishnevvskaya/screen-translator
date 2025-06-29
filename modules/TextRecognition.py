from PyQt5 import QtCore
from paddleocr import PaddleOCR
import numpy as np
import pyautogui

from .Utils import Utils
from .Thread import ModelLoadedThread

model_dir = r"./paddle_models" 
_ocr_models = {}
_active_thread = {}

def get_ocr_model(lang_value, callback=None):
    if lang_value in _ocr_models:
        callback and callback(_ocr_models[lang_value])
        return _ocr_models[lang_value]
    
    if lang_value not in _active_thread:
        loader = ModelLoadedThread(lang_value)
        _active_thread[lang_value] = loader

        def handle_loaded(model):
            _ocr_models[lang_value] = model
            _active_thread.pop(lang_value, None)
            callback and callback(model)
                
        loader.loaded.connect(handle_loaded)
        loader.finished.connect(loader.deleteLater)
        loader.start()

    elif callback:
        _active_thread[lang_value].loaded.connect(callback)

    return None
    
class TextRecognition:
    def __init__(self, lang_key):
        self.ocr_model = None
        get_ocr_model(Utils.get_en_languages()[lang_key], lambda model: setattr(self, 'ocr_model', model))
    
    def on_model_loaded(self, model):
        self.ocr_model = model
    
    def get_window_text(self, region):
        if not self.ocr_model:
            return ''
        
        rect = QtCore.QRect(region[0], region[1]).normalized()
        region_tuple = (rect.x(), rect.y(), rect.width(), rect.height())

        screenshot = pyautogui.screenshot(region=region_tuple)
        result = self.ocr_model.predict(np.array(screenshot))

        texts = ' '.join(result[0]['rec_texts'])
        return texts