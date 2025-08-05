from django.urls import path
from .views_site import (
    courses_list, course_detail, course_create,
    user_login, user_logout, user_register, enroll_course,
)

urlpatterns = [
    path('', courses_list, name='courses_list'),
    path('course/<int:pk>/', course_detail, name='course_detail'),
    path('course/create/', course_create, name='course-create'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('course/<int:pk>/enroll/', enroll_course, name='enroll-course'),
]