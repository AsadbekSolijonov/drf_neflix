from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    img = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.phone}"
