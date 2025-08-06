from django import forms
from .models import CustomUser

# Asosiy umumiy forma
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  # role ni bu yerda olmaymiz

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Student uchun maxsus forma
class StudentRegisterForm(RegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'STUDENT'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Teacher uchun maxsus forma
class TeacherRegisterForm(RegisterForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'TEACHER'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
