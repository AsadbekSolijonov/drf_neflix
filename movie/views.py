from email.policy import HTTP

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Genre, Content
from movie.serializers import GenreSerializer, ContentSerializer


# CRUD
@api_view(['GET', 'POST'])
def genre_list_or_create(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def genre_retrive_update_or_delete(request, pk):
    try:
        genre = Genre.objects.get(id=pk)
    except Genre.DoesNotExist:
        return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        genre.delete()
        return Response({"detail": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_contents(request):
    contents = Content.objects.all()
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)
