from django.urls import path
from .views import (
    register_student_view, register_teacher_view,
    login_student_view, login_teacher_view,custom_logout_view
    # oldingi API-based viewlar ham kerak
)

urlpatterns = [
    path('register/student/', register_student_view, name='register_student_html'),
    path('register/teacher/', register_teacher_view, name='register_teacher_html'),
    path('login/student/', login_student_view, name='login_student_html'),
    path('login/teacher/', login_teacher_view, name='login_teacher_html'),
    path('logout/', custom_logout_view, name='logout'),
    path('users/logout/', custom_logout_view, name='logout'),
]
