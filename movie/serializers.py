from django.contrib.auth.models import User
from rest_framework import serializers

from movie.models import Genre, Content

User


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=30, allow_blank=True)
    last_name = serializers.CharField(max_length=30, allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15, required=True)
    image = serializers.ImageField(allow_empty_file=True, allow_null=True)

    def to_representation(self, instance):
        request = self.context.get('request')

        profile = instance.profile if hasattr(instance, 'profile') else None
        phone = profile.phone if profile else None
        img = profile.img if profile else None
        img_url = img.url if img else None

        full_img_url = request.build_absolute_uri(img_url) if request and img_url else img_url

        return {
            "username": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "profile": {
                "phone": phone,
                "image": full_img_url
            }
        }
