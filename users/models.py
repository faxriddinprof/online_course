from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'O‘quvchi'),
        ('TEACHER', 'O‘qituvchi'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
