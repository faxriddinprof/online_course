from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterStudentView,
    RegisterTeacherView,
    StudentTokenObtainPairView,
    TeacherTokenObtainPairView,
    ProfileView
)

urlpatterns = [
    # === Ro'yxatdan o'tish ===
    path('register/student/', RegisterStudentView.as_view(), name='register_student'),
    path('register/teacher/', RegisterTeacherView.as_view(), name='register_teacher'),

    # === Login (JWT token) ===
    path(
        'login/student/', 
        StudentTokenObtainPairView.as_view(),
        name='login_student'
    ),
    path(
        'login/teacher/', 
        TeacherTokenObtainPairView.as_view(),
        name='login_teacher'
    ),

    # Tokenni yangilash
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profil (hozirgi user)
    path('me/', ProfileView.as_view(), name='user_profile'),
]