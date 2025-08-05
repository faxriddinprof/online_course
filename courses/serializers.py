from rest_framework import serializers
from .models import Category, Course, Section, Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Section
        fields = ['id', 'title', 'modules']

class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image', 'author', 'category', 'sections']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']