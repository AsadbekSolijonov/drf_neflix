from django.contrib import admin

from movie.models.account import Profile
from movie.models.movie import Genre, Content, WatchedHistory

admin.site.register([Genre, Content, Profile, WatchedHistory])
