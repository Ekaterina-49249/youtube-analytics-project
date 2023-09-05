import json
import os
from googleapiclient.discovery import build
from src.utils import printj


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('YT_API_KEY')  # ключ из переменной окружение
    youtube = build('youtube', 'v3', developerKey=api_key)  # объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

    def __str__(self):
        return f"{self.title}({self.url})"

    def __add__(self, other):
        """Сложение подписчиков двух классов"""
        return self.view_count + other.view_count

    def __sub__(self, other):
        """Разность подписчиков двух классов"""
        return self.view_count - other.view_count

    def __lt__(self, other):
        """Сравнение классов по кол-ву подписчиков"""
        return self.view_count < other.view_count

    def __gt__(self, other):
        """Сравнение классов по кол-ву подписчиков"""
        return self.view_count > other.view_count

    def __ge__(self, other):
        """Сравнение классов по кол-ву подписчиков"""
        return self.view_count >= other.view_count

    def __le__(self, other):
        """Сравнение кассов по кол-ву подписчиков"""
        return self.view_count <= other.view_count

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.channel["items"][0]["snippet"]["title"]

    @property
    def description(self):
        return self.channel["items"][0]["snippet"]["description"]

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def subscriber_count(self):
        return int(self.channel["items"][0]["statistics"]["subscriberCount"])

    @property
    def video_count(self):
        return int(self.channel["items"][0]["statistics"]["videoCount"])

    @property
    def view_count(self):
        return int(self.channel["items"][0]["statistics"]["viewCount"])

    def to_json(self, file_name):
        """ Метод, сохраняющий в файл значение атрибутов экземпляра Channel"""
        with open(file_name, "w", encoding="utf-8") as file:
            argdict = {
                "title": self.title,
                "url": self.url,
                "subscriber_count": self.subscriber_count,
                "id": self.__channel_id,
                "description": self.description,
                "video_count": self.video_count,
                "view_count": self.view_count
            }
            json.dump(argdict, file, ensure_ascii=False)

    def print_info(self) -> None:
        """Метод выводит в консоль информацию о канале."""
        printj(self.channel)
