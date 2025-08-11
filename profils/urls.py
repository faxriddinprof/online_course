from django.urls import path
from .views import profile_view, my_courses_view

urlpatterns = [
    path('', profile_view, name='profile'),
    path('my-courses/', my_courses_view, name='my_courses'),
]
