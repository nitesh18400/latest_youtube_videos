import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from video_service.serializers import VideoSerializer, GoogleAPIClientKeySerializer
from video_service.service import VideoService
from .models import Video

HOME_HTML = "home.html"


@api_view(['GET'])
def get_video_data(request):
    try:
        # Retrieve all videos from the database, sorted by published datetime in descending order
        videos = VideoService.get_singleton().fetch_videos()

        # Paginate the results
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        paginator = Paginator(videos, page_size)
        videos_page = paginator.page(page)

        # Serialize the paginated videos
        serializer = VideoSerializer(videos_page, many=True)

        # Calculate additional pagination information
        current_page = videos_page.number
        total_pages = paginator.num_pages
        first_page = 1
        last_page = total_pages

        # Construct the response data
        response_data = {
            'videos': serializer.data,
            'current_page': current_page,
            'first_page': first_page,
            'last_page': last_page,
        }

        return Response(response_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_api_key(request):
    try:
        serializer = GoogleAPIClientKeySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def search_videos(request):
    query = request.GET.get('query', '')
    if query:
        # Split the query into individual words
        query_words = query.lower().split()

        # Initialize dictionary to store video IDs and their similarity scores
        similarity_scores = {}

        # Iterate over all videos
        for video in Video.objects.filter(published_at__day=datetime.datetime.now().day).all():
            # Convert video title and description to lowercase and split into words
            title_words = set(video.title.lower().split())
            description_words = set(video.description.lower().split())

            # Calculate Jaccard similarity for title and description
            title_similarity = len(set(query_words).intersection(title_words)) / len(
                set(query_words).union(title_words))
            description_similarity = len(set(query_words).intersection(description_words)) / len(
                set(query_words).union(description_words))

            # Take the maximum similarity score between title and description
            similarity_scores[video.id] = max(title_similarity, description_similarity)

        # Sort video IDs based on similarity score in descending order
        sorted_video_ids = sorted(similarity_scores.keys(), key=lambda x: similarity_scores[x], reverse=True)
        sorted_video_ids = [str(video_id) for video_id in sorted_video_ids if similarity_scores[video_id] > 0]

        # Retrieve videos based on sorted video IDs
        videos = Video.objects.filter(id__in=sorted_video_ids)
        videos = VideoSerializer(videos, many=True)

        # Serialize the results
        data = videos.data
        return JsonResponse({'videos': data})
    else:
        return JsonResponse({'error': 'Query parameter "query" is required'}, status=400)


def home(request):
    return render(request, HOME_HTML)


def latest_youtube_videos(request):
    return render(request, HOME_HTML, context={"show_latest_videos": True})


def video_search(request):
    return render(request, HOME_HTML, context={"show_search_videos": True})


def add_key(request):
    return render(request, HOME_HTML, context={"show_add_key": True})
