from django.contrib.auth import logout
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models.account import User
from movie.models.movie import Content
from movie.permissions import TimeCheckerPermission, IsAuthenticatedOrReadOnly, IsOwnerOrSuperuser, IsAuthenticated
from movie.serializers.account import UserProfileSerializer, UserSerializer, UserStatisticsSerializer, \
    LoginUserSerializer, ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer
from movie.serializers.movie import ContentStatisticsSerializer


@api_view(['GET', 'POST'])
def user_list_or_create(request, format=None):
    if request.method == 'GET':
        users = User.objects.select_related('profile')
        serializer = UserProfileSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        print(serializer.initial_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def user_retrive_update_or_delete(request, pk, format=None):
    try:
        user = User.objects.select_related('profile').get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(user, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])  # list yoki POST
@permission_classes([TimeCheckerPermission])
def user_nested_list_or_create(request, format=None):
    if request.method == 'GET':
        users = User.objects.select_related('profile')
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', "DELETE"])  # Retrive, Update, Delete
@permission_classes([IsAuthenticatedOrReadOnly])
def user_nested_retrieve_update_or_delete(request, pk, format=None):
    permission = IsOwnerOrSuperuser()
    try:
        user = User.objects.select_related('profile').get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User object not found"}, status=status.HTTP_404_NOT_FOUND)

    if not permission.has_object_permission(request, None, user):
        return Response({"message": "You don't have permissions this action"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={"request": request, "user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, context={"request": request, "user": user},
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        if request.user != user:
            return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


class UserStatisticsView(APIView):
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]  # Request level permission, Object level Permission

    def get(self, requst):
        films = User.objects.annotate(watched_films_count=Count('watched_history')).order_by('-watched_films_count')
        contents = Content.objects.annotate(film_watched_count=Count('watched_history')).order_by('-film_watched_count')

        serializer = UserStatisticsSerializer(films, many=True)
        contents = ContentStatisticsSerializer(contents, many=True)
        films = films.aggregate(watched_films=Sum('watched_films_count'))
        return Response({
            "watched_films": films['watched_films'],
            "contents": contents.data,
            "watched_films_count_by_each_user": serializer.data
        })


class RegisterUserProfile(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response({
            "message": "User successfully created",
            "user": serializer.data,
            "token": str(token.key)
        }, status=status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "User logged out!"})


class ResetPasswordRequestAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Emailga maxsus kod yuborildi!"})


class ResetPasswordConfirmAPIView(APIView):

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password muvaffaqiyatli o'zgardi!"})


class AccountUserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]
