from datetime import datetime, timedelta
from typing import List

from googleapiclient.discovery import build

from video_service.constants import SEARCH_QUERY
from video_service.models import GoogleAPIClientKey
from video_service.service import YouTubeAPIService, VideoService
from video_service.serviceBase import ServiceBase


class FetchVideoService(ServiceBase):

    def __init__(self):
        super().__init__()
        self._youtube_api_service: YouTubeAPIService = YouTubeAPIService.get_singleton()
        self._video_service: VideoService = VideoService.get_singleton()
        self.api_key: GoogleAPIClientKey = self.get_active_api_key()
        self.api_keys: List[GoogleAPIClientKey] = self.get_all_active_api_keys()

    @classmethod
    def create_singleton(cls):
        return FetchVideoService()

    def get_active_api_key(self):
        api_key_object = self._youtube_api_service.get_active_api_key()
        if api_key_object:
            return api_key_object.api_key
        else:
            raise Exception("No active API key found")

    def get_all_active_api_keys(self):
        api_keys = self._youtube_api_service.get_all_active_api_keys()
        if api_keys:
            return list(api_keys)
        else:
            raise Exception("No active API keys found")

    def fetch_and_store_videos(self, search_query: str = SEARCH_QUERY, max_results: int = 10):
        response = None
        for api_key in self.api_keys:
            youtube = build('youtube', 'v3', developerKey=api_key)
            request = youtube.search().list(
                part='id,snippet',
                type='video',
                order='date',
                q=search_query,
                publishedAfter=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                maxResults=max_results
            )
            response = request.execute()
            print("response:", response)
            try:
                if response['items']:
                    break
            except Exception as e:
                print(f"Error occurred while fetching videos: {str(e)}")
                if 'quota' in response.lower():
                    continue
                response = None
                break
        if response is not None:
            self.store_videos(response)
        return "Videos fetched and stored successfully."

    def store_videos(self, response):
        try:
            for item in response['items']:
                snippet = item['snippet']
                video_title = snippet['title']
                description = snippet['description']
                published_at = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                thumbnail_url = snippet['thumbnails']['high']['url']
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
            print(f"Error occurred while storing videos: {str(e)}, Response: {response}")
