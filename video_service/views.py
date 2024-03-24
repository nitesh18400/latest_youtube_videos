from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from video_service.models import Video
from video_service.serializers import VideoSerializer, GoogleAPIClientKeySerializer


@api_view(['GET'])
def get_video_data(request):
    try:
        # Retrieve all videos from the database, sorted by published datetime in descending order
        videos = Video.objects.all().order_by('-published_at')

        # Paginate the results
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        paginator = Paginator(videos, page_size)
        videos_page = paginator.page(page)

        # Serialize the paginated videos
        serializer = VideoSerializer(videos_page, many=True)

        return Response(serializer.data)
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