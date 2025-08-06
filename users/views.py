from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import StudentRegisterForm, TeacherRegisterForm
from .models import CustomUser


def register_student_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_student_html')
    else:
        form = StudentRegisterForm()
    return render(request, 'registr/register_student.html', {'form': form})


def register_teacher_view(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_teacher_html')
    else:
        form = TeacherRegisterForm()
    return render(request, 'registr/register_teacher.html', {'form': form})


def login_student_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'STUDENT':
            login(request, user)
            return redirect('courses_list')  # sahifani istalgan joyga yo'naltiring
        else:
            error = "Login yoki parol noto'g'ri yoki siz o‘quvchi emassiz."
    return render(request, 'registr/login_student.html', {'error': error})


def login_teacher_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role == 'TEACHER':
            login(request, user)
            return redirect('courses_list')  # sahifani istalgan joyga yo'naltiring
        else:
            error = "Login yoki parol noto'g'ri yoki siz o‘qituvchi emassiz."
    return render(request, 'registr/login_teacher.html', {'error': error})


def custom_logout_view(request):
    if request.user.is_authenticated:
        role = request.user.role
        logout(request)
        if role == 'STUDENT':
            return redirect('login_student_html')
        elif role == 'TEACHER':
            return redirect('login_teacher_html')
    return redirect('login')  # fallback (agar login bo‘lmagan bo‘lsa)
