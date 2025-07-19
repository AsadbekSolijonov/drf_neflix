from django.urls import path
from movie import views

urlpatterns = [
    path('', views.genre_list_or_create),
    path('<int:pk>/', views.genre_retrive_update_or_delete),
    path('contents/', views.get_contents)
]
