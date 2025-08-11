from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.jpg', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} profili"
