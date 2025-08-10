from django import forms
from .models import Course, Section, Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description', 'image']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'video', 'youtube_url', 'description']