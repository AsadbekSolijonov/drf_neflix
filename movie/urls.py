from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from movie.views.account import user_list_or_create, user_retrive_update_or_delete, user_nested_list_or_create, \
    user_nested_retrieve_update_or_delete, UserStatisticsView, RegisterUserProfile, LoginUserAPIView, \
    AccountUserListAPIView, LogoutUserAPIView, ResetPasswordRequestAPIView, ResetPasswordConfirmAPIView
from movie.views.movie import GenreViewSet, genre_list_or_create, genre_retrive_update_or_delete, \
    content_list_or_create, content_retrive_update_or_delete, WatchedHistoryView, WatchedHistoryDestroyView

router = DefaultRouter()
router.register('cbv-user_viewset', GenreViewSet)

urlpatterns = [
    path('', genre_list_or_create, name='genre_list_or_create'),
    path('<int:pk>/', genre_retrive_update_or_delete),
    path('contents/', content_list_or_create),
    path('contents/<int:pk>/', content_retrive_update_or_delete),
    path('users/', user_list_or_create),
    path('users/<int:pk>/', user_retrive_update_or_delete),
    path('nt-users/', user_nested_list_or_create),
    path('nt-users/<int:pk>/', user_nested_retrieve_update_or_delete),
    # path('cbv/', GenreListView.as_view()),
    path('history/', WatchedHistoryView.as_view()),
    path('history/<int:pk>/delete/', WatchedHistoryDestroyView.as_view()),
    path("user-statistics/", UserStatisticsView.as_view()),

    # APIView Resgister
    path('register/', RegisterUserProfile.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('list-apiview-users/', AccountUserListAPIView.as_view(), name='list_api_view_users'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordRequestAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', ResetPasswordConfirmAPIView.as_view(), name='reset_password_confirm'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
