from video_service.models import GoogleAPIClientKey
from video_service.repository import GoogleAPIClientKeyRepository, VideoRepository
from video_service.serviceBase import ServiceBase


class YouTubeAPIService(ServiceBase):

    @classmethod
    def create_singleton(cls):
        return YouTubeAPIService()

    @staticmethod
    def get_active_api_key():
        return GoogleAPIClientKeyRepository.get_active_api_key()

    @staticmethod
    def deactivate_api_key(api_key: GoogleAPIClientKey):
        return GoogleAPIClientKeyRepository.deactivate_api_key(api_key)


class VideoService(ServiceBase):

    @classmethod
    def create_singleton(cls):
        return VideoService()

    @staticmethod
    def fetch_video(yt_unique_id):
        return VideoRepository.fetch_video(yt_unique_id)

    @staticmethod
    def create_video(yt_unique_id, title, description, published_at, thumbnail_url):
        return VideoRepository.create_video(yt_unique_id, title, description, published_at, thumbnail_url)

    @staticmethod
    def update_video(video, title=None, description=None, published_at=None, thumbnail_url=None):
        return VideoRepository.update_video(video, title, description, published_at, thumbnail_url)
