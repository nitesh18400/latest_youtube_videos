# youtube_api/repositories.py

from .models import GoogleAPIClientKey, Video
from .repoBase import RepoBase


class GoogleAPIClientKeyRepository(RepoBase):

    @classmethod
    def create_singleton(cls):
        return GoogleAPIClientKeyRepository()

    @staticmethod
    def get_active_api_key():
        return GoogleAPIClientKey.objects.filter(active=True).first()

    @staticmethod
    def deactivate_api_key(api_key: GoogleAPIClientKey):
        api_key.active = False
        api_key.save()


class VideoRepository(RepoBase):

    @classmethod
    def create_singleton(cls):
        return VideoRepository()

    @staticmethod
    def create_video(yt_unique_id, title, description, published_at, thumbnail_url):
        return Video.objects.create(
            yt_unique_id=yt_unique_id,
            title=title,
            description=description,
            published_at=published_at,
            thumbnail_url=thumbnail_url
        )

    @staticmethod
    def update_video(video, title=None, description=None, published_at=None, thumbnail_url=None):
        if title:
            video.title = title
        if description:
            video.description = description
        if published_at:
            video.published_at = published_at
        if thumbnail_url:
            video.thumbnail_url = thumbnail_url
        video.save()

    @staticmethod
    def fetch_video(yt_unique_id):
        return Video.objects.filter(yt_unique_id=yt_unique_id).first()
