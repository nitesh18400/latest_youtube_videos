from django.urls import path

from video_service import views

urlpatterns = [
    # UI Urls
    path('', views.home, name='home'),
    path('latest-videos/', views.latest_youtube_videos, name='latest-videos'),
    path('video-search/', views.video_search, name='video-search'),
    path('add-key/', views.add_key, name='add-key'),

    # API Urls
    path('api/videos/', views.get_video_data, name='video-list'),
    path('api/add-key/', views.add_api_key, name='add-api-key'),
    path('api/search/', views.search_videos, name='search_videos'),

]
