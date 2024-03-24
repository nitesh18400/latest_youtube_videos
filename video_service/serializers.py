from rest_framework import serializers

from video_service.models import Video, GoogleAPIClientKey


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class GoogleAPIClientKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleAPIClientKey
        fields = '__all__'
