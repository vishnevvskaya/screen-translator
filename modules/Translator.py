from deep_translator import GoogleTranslator, MyMemoryTranslator

from .Utils import *
from .Logger import *

class Translator:
    def __init__(self, provider, from_lang_index, to_lang_index):
        self.provider = provider

        if provider == 'Google Translate':
            language_items = list(Utils.get_en_languages().values())
        elif provider == 'MyMemoryTranslator':
            language_items = list(Utils.get_memory_tl_languages().values())

        self.from_lang = language_items[from_lang_index]
        self.to_lang =language_items[to_lang_index]
        logger.debug(f"Language pair ({self.provider}): {self.from_lang} -> {self.to_lang}")
    
    def set_translator(self, text):
        '''Launch the selected translator'''
        if not text.strip():
            return ''
        
        try:
            if self.provider == 'Google Translate':
                return self.google_tl(text)
            elif self.provider == 'MyMemoryTranslator':
                return self.memory_tl(text)
        except Exception as e:
            logger.error(f'Translation error ({self.provider}): {e}')
            return ''

    def google_tl(self, text):
        '''Translation via Google Translate'''
        try:
            translated = GoogleTranslator(source=self.from_lang, target=self.to_lang).translate(text.strip())
            return translated
        except Exception as e:
            logger.error(f'Translation failed ({self.provider}): {e}')
            raise
    
    def memory_tl(self, text):
        '''Translation via MyMemoryTranslator'''
        chunks = [text[i:i+499] for i in range(0, len(text), 499)]
        translated_chunks = []

        for chunk in chunks:
            try:
                translated = MyMemoryTranslator(source=self.from_lang, target=self.to_lang).translate(chunk)
                translated_chunks.append(translated)
            except Exception as e:
                logger.error(f'Chunk translation failed ({self.provider}): {e}')
                raise
        return ' '.join(translated_chunks)