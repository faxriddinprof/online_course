from django.urls import path

from .views import (
    courses_list, course_detail, course_create,
    enroll_course,
)

urlpatterns = [
    path('', courses_list, name='courses_list'),
    path('course/<int:pk>/', course_detail, name='course_detail'),
    path('course/<int:pk>/section/<int:section_id>/module/<int:module_id>/', course_detail, name='course_module_detail'),
    path('course/create/', course_create, name='course-create'),
    path('course/<int:pk>/enroll/', enroll_course, name='enroll-course'),
]
