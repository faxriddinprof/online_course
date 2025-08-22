from django.urls import path

from .views import (
    courses_list, 
    course_detail, 
    course_create,
    enroll_course, 
    section_create,
    module_create,
    course_content,
    teacher_students,
    api_complete_module
)

urlpatterns = [
    path('', courses_list, name='courses_list'),
    path('course/<int:pk>/', course_detail, name='course_detail'),
    path('course/<int:pk>/section/<int:section_id>/module/<int:module_id>/', course_detail, name='course_module_detail'),
    path('course/create/', course_create, name='course-create'),
    path('course/<int:pk>/enroll/', enroll_course, name='enroll-course'),

    path('course/<int:course_id>/section/create/', section_create, name='section-create'),
    path('section/<int:section_id>/module/create/', module_create, name='module-create'),
    
     # ✅ yangi (course_content uchun to'liq marshrutlar)
    path('course/<int:pk>/content/', course_content, name='course_content'),
    path('course/<int:pk>/content/section/<int:section_id>/', course_content, name='course_content_section'),
    path('course/<int:pk>/content/section/<int:section_id>/module/<int:module_id>/', course_content, name='course_content_module'),

    path('teacher/students/', teacher_students, name='teacher_students'),


    #  ✅ Module’ni “completed” qilish uchun API
    path('api/module/<int:module_id>/complete/', api_complete_module, name='api_module_complete'),
]
