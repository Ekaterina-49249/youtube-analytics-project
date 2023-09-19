from src.request_youtube import RequestYoutube


class Video(RequestYoutube):

    def __init__(self, id_video: str) -> None:
        """Инициализация экземпляра класса Video"""

        try:
            self.__id_video = id_video
            self.video_request = self.get_service().youtube.videos().list(id=self.__id_video,
                                                                          part='snippet,statistics').execute()
            self.title = self.video_request["items"][0]["snippet"]["title"]
            self.url = f"https://www.youtube.com/watch?v={self.__id_video}"
            self.like_count = int(self.video_request["items"][0]["statistics"]["likeCount"])
            self.number_views = int(self.video_request["items"][0]["statistics"]["viewCount"])

        except Exception as e:
            print(e)

            self.__id_video = id_video
            self.title = None
            self.like_count = None
            self.number_views = None
            self.url = None

    # @property
    # def id_video(self):
    #     return self.__id_video
    #
    # @property
    # def title(self):
    #     return self.video_request["items"][0]["snippet"]["title"]
    #
    # @title.setter
    # def title(self, value):
    #     self.title = value
    #
    # def __str__(self):
    #     return self.title
    #
    # @property
    # def url(self):
    #     return f"https://www.youtube.com/watch?v={self.__id_video}"
    #
    # @url.setter
    # def url(self, value):
    #     self.url = value
    #
    # @property
    # def number_views(self):
    #     return int(self.video_request["items"][0]["statistics"]["viewCount"])
    #
    # @number_views.setter
    # def number_views(self, value):
    #     self.number_views = value
    #
    # @property
    # def like_count(self):
    #     return int(self.video_request["items"][0]["statistics"]["likeCount"])
    #
    # @like_count.setter
    # def like_count(self, value):
    #     self.like_count = value


class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.__id_playlist = id_playlist
        self.__plvideo = RequestYoutube.youtube.playlistItems().list(
            part='status',
            videoId=id_video,
            playlistId=id_playlist).execute()
        result_count = int(self.__plvideo["pageInfo"]["totalResults"])
        if result_count == 0:
            raise ValueError("Нет видео в плейлисте")

    @property
    def id_playlist(self):
        return self.__id_playlist
