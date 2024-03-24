from celery import shared_task


@shared_task
def my_task():
    print('Hello from Celery!')


@shared_task
def fetch_latest_youtube_videos():
    print("Fetching and storing videos...")
    from video_service.fetchVideoSerive import FetchVideoService
    fetch_video_service: FetchVideoService = FetchVideoService.get_singleton()
    fetch_video_service.fetch_and_store_videos()
    print("Fetched and stored videos successfully.")
