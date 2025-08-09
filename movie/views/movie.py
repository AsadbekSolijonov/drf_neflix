from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from movie.models.movie import WatchedHistory, Genre, Content
from movie.permissions import IsSuperUser, IsAuthenticated
from django.db.models import Q, Count, Sum

from movie.serializers.movie import GenreSerializer, ContentSerializer, WatchedHistorySerializer


# CRUD
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def genre_list_or_create(request, format=None):
    if request.method == 'GET':
        genres = Genre.objects.all()
        search = request.query_params.get('search', None)
        if search:
            genres = genres.filter(name__icontains=search)
        serializer = GenreSerializer(genres, many=True)
        content = Content.objects.filter(genres__in=genres).count()
        return Response({
            "total_genres": genres.count(),
            "total_films": content,
            "genres": serializer.data},
            status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def genre_retrive_update_or_delete(request, pk, format=None):
    try:
        genre = Genre.objects.get(id=pk)
    except Genre.DoesNotExist:
        return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genre.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def content_list_or_create(request, format=None):
    if request.method == 'GET':
        genre = request.query_params.get('genre')
        director = request.query_params.get('director')
        title = request.query_params.get('title')
        desc = request.query_params.get('desc')

        filters = Q()
        if genre:
            filters &= Q(genres__name__icontains=genre)

        if director:
            filters &= Q(director__icontains=director)

        if title:
            filters &= Q(title__icontains=title)

        if desc:
            filters &= Q(description__icontains=desc)

        contents = Content.objects.filter(filters).distinct()

        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def content_retrive_update_or_delete(request, pk, format=None):
    try:
        content = Content.objects.get(id=pk)
    except Content.DoesNotExist:
        return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        content.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


# APIVIew, Generics(), Concrate Generics(), ViewSet, ModelViewSet

class GenreListView(APIView):  # Lis
    def get(self, request, format=None):
        genres = Genre.objects.all()
        search = request.query_params.get('search', None)
        if search:
            genres = genres.filter(name__icontains=search)
        serializer = GenreSerializer(genres, many=True)
        content = Content.objects.filter(genres__in=genres).count()
        return Response({
            "total_genres": genres.count(),
            "total_films": content,
            "genres": serializer.data},
            status=status.HTTP_200_OK)


class GenreViewSet(ModelViewSet):  # CRUD
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsSuperUser]


class WatchedHistoryView(APIView):
    def get(self, request):
        histories = WatchedHistory.objects.select_related('user', 'content').filter(is_delete=False)
        serializer = WatchedHistorySerializer(histories, many=True)
        films = WatchedHistory.objects.aggregate(
            watched_films_count=Count('id'),
            history_clear=Count('id', filter=Q(is_delete=True))
        )
        return Response({
            "watched_films_count": films['watched_films_count'],
            "history_clear": films['history_clear'],
            "histories": serializer.data
        })

    def post(self, request):
        serializer = WatchedHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchedHistoryDestroyView(APIView):

    def get_object(self, pk):
        return get_object_or_404(WatchedHistory, id=pk, is_delete=False)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.is_delete = True
        obj.save()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)
