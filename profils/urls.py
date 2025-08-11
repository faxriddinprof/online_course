from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
