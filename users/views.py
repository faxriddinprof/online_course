from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from .serializers import (
    UserSerializer,
    RegisterStudentSerializer,
    RegisterTeacherSerializer
)
from .permissions import IsStudent, IsTeacher


class RegisterStudentView(generics.CreateAPIView):
    """
    O‘quvchi (student) ro‘yxatdan o‘tish endpoint’i.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterStudentSerializer


class RegisterTeacherView(generics.CreateAPIView):
    """
    O‘qituvchi (teacher) ro‘yxatdan o‘tish endpoint’i.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterTeacherSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT login jarayonida foydalanuvchi rolini tekshiradi.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # View’dan kelgan expected_role ni tekshirish
        expected_role = self.context['view'].expected_role
        if user.role != expected_role:
            raise serializers.ValidationError(
                f"Siz {expected_role.lower()} sifatida login qilishingiz kerak."
            )

        # Qo‘shimcha ma’lumot sifatida user profili
        data.update({
            'user': UserSerializer(user).data
        })
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWT login jarayonida foydalanuvchi rolini tekshiradi.
    """
    serializer_class = CustomTokenObtainPairSerializer
    expected_role = None  # default

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['view'] = self
        return context

# Har bir rol uchun alohida subclasslar:
class StudentTokenObtainPairView(CustomTokenObtainPairView):
    expected_role = 'STUDENT'

class TeacherTokenObtainPairView(CustomTokenObtainPairView):
    expected_role = 'TEACHER'


class ProfileView(generics.RetrieveAPIView):
    """
    Hozirgi authenticated foydalanuvchi profilini qaytaradi.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user