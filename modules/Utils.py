import json

class Utils:
    def get_en_languages():
        with open('./assets/settings.json', 'r', encoding='utf-8') as settings:
            data = json.load(settings)

            return data.get('languages', {}).get('en', {})
        
    def get_ru_languages():
        with open('./assets/settings.json', 'r', encoding='utf-8') as settings:
            data = json.load(settings)

            return data.get('languages', {}).get('ru', {})