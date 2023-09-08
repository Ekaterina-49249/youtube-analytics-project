import os
from googleapiclient.discovery import build


class RequestYoutube:
    api_key = os.getenv('YT_API_KEY')  # ключ из переменной окружение
    youtube = build('youtube', 'v3', developerKey=api_key)  # объект для работы с API

    @classmethod
    def get_service(cls):
        return cls.youtube





