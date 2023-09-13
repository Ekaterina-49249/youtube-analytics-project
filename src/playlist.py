import isodate

from src.request_youtube import RequestYoutube
from datetime import timedelta


class PlayList(RequestYoutube):

    def __init__(self, id_playlist):
        self.__id_playlist = id_playlist
        self.info_json = self.get_service().playlists().list(id=self.__id_playlist, part='snippet').execute()
        self.title = self.info_json['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__id_playlist}"

        # данные о плейлисте(кол-во видео, дата публикации)
        self.playlist_videos = self.get_service().playlistItems().list(part='contentDetails',
                                                                       playlistId=self.__id_playlist,
                                                                       maxResults=50,
                                                                       ).execute()
        # список id всех видео из плейлиста
        video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        # данные о видео, длительность, кол-во просмотров, лайков
        self.playlist_videos_duration = self.get_service().videos().list(part='contentDetails,statistics',
                                                                         id=','.join(video_ids)
                                                                         ).execute()

    @property
    def total_duration(self):
        """Метод возвращает общую длительность плейлиста"""
        duration = timedelta()
        # получение длительности всех видео
        for video in self.playlist_videos_duration['items']:
            duration += isodate.parse_duration(video['contentDetails']['duration'])
        return duration

    def show_best_video(self):
        """Метод возвращает ссылку на самое популярное видео из плейлиста"""
        max_likes = 0
        best_video = ''

        # поиск самого популярного видео
        for video in self.playlist_videos_duration['items']:
            # получение кол-ва лайков
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                max_likes = likes
                # получение id самого популярного видео
                best_video = video["id"]
        return f"https://youtu.be/{best_video}"
