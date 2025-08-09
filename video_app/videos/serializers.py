from rest_framework import serializers
from .models import Video, VideoFile

class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ['id', 'file', 'quality']


class VideoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'username', 'name', 'total_likes', 'created_at', 'files']