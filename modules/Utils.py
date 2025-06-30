from pathlib import Path
import json

class Utils:
    SETTINGS_PATH = Path('./assets/settings.json')
    @staticmethod
    def get_en_languages():
        with open(Utils.SETTINGS_PATH, 'r', encoding='utf-8') as settings:
            data = json.load(settings)
            return data.get('languages', {}).get('en', {})
    
    @staticmethod
    def get_ru_languages():
        with open(Utils.SETTINGS_PATH, 'r', encoding='utf-8') as settings:
            data = json.load(settings)
            return data.get('languages', {}).get('ru', {})