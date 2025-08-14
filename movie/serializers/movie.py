from rest_framework import serializers
from movie.models.movie import Content, Genre, WatchedHistory


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    # contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['name', 'id']


class WatchedHistorySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    content_name = serializers.StringRelatedField(source='content')

    class Meta:
        model = WatchedHistory
        fields = ('id', 'watched_at', 'user', 'content', 'username', 'content_name', 'is_delete')
        read_only_fields = ('id', 'watched_at')
        extra_kwargs = {
            "user": {"write_only": True},
            "content": {"write_only": True},
        }

    def get_username(self, obj):
        full_name = obj.user.username
        if obj.user.first_name and obj.user.last_name:
            full_name = obj.user.get_full_name()

        return full_name


class ContentStatisticsSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    film_watched_count = serializers.CharField(read_only=True)