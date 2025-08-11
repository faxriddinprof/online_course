from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

User = get_user_model()

def default_profile_image():
    return 'img/default.png'  # static/img ichida bo‘ladi

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def image_or_default(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return os.path.join('/static/', default_profile_image())

    def __str__(self):
        return f"{self.user.username} profili"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
