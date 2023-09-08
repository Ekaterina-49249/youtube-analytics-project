from src.request_youtube import RequestYoutube


class Video(RequestYoutube):

    def __init__(self, id_video):
        self.__id_video = id_video
        self.__video = RequestYoutube.youtube.videos().list(id=self.__id_video, part='snippet,statistics').execute()

    @property
    def id_video(self):
        return self.__id_video

    @property
    def title(self):
        return self.__video["items"][0]["snippet"]["title"]

    def __str__(self):
        return self.title

    @property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.__id_video}"

    @property
    def number_views(self):
        return int(self.__video["items"][0]["statistics"]["viewCount"])

    @property
    def like_count(self):
        return int(self.__video["items"][0]["statistics"]["likeCount"])


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
