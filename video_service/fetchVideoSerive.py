from datetime import datetime

from googleapiclient.discovery import build

from video_service.constants import SEARCH_QUERY
from video_service.service import YouTubeAPIService, VideoService
from video_service.serviceBase import ServiceBase


class FetchVideoService(ServiceBase):

    def __init__(self):
        super().__init__()
        self.api_key = self.get_active_api_key()
        self._youtube_api_service: YouTubeAPIService = YouTubeAPIService.get_singleton()
        self._video_service: VideoService = VideoService.get_singleton()

    @classmethod
    def create_singleton(cls):
        return FetchVideoService()

    def get_active_api_key(self):
        api_key_object = self._youtube_api_service.get_active_api_key()
        if api_key_object:
            return api_key_object.api_key
        else:
            raise Exception("No active API key found")

    def fetch_and_store_videos(self, search_query: str = SEARCH_QUERY, max_results: int = 10):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        request = youtube.search().list(
            part='snippet',
            type='video',
            q=search_query,
            maxResults=max_results
        )
        response = request.execute()
        self.store_videos(response)
        return "Videos fetched and stored successfully."

    def store_videos(self, response):
        try:
            for item in response['items']:
                snippet = item['snippet']
                video_title = snippet['title']
                description = snippet['description']
                published_at = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                thumbnail_url = snippet['thumbnails']['default']['url']
                yt_unique_id = item['id']['videoId']

                if self._video_service.fetch_video(yt_unique_id):
                    print("Video already exists in the database. Skipping...")
                    continue

                self._video_service.create_video(
                    yt_unique_id=yt_unique_id,
                    title=video_title,
                    description=description,
                    published_at=published_at,
                    thumbnail_url=thumbnail_url
                )
        except Exception as e:
            if 'quota' in str(e).lower():
                self._youtube_api_service.deactivate_api_key(self.api_key)
            print(f"Error occurred while storing videos: {str(e)}, Response: {response}")
