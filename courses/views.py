from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from courses.models import Course, Category
from courses.forms import CourseForm
from users.models import CustomUser
from users.serializers import UserSerializer
from django.views.decorators.http import require_POST




def courses_list(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    courses = Course.objects.all()
    categories = Category.objects.all()
    if category:
        courses = courses.filter(category__name=category)
    if search:
        courses = courses.filter(title__icontains=search)
    return render(request, 'courses_list.html', {
        'courses': courses,
        'categories': categories,
    })

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_detail.html', {'course': course})

@login_required
def course_create(request):
    if not request.user.role == 'TEACHER':
        return redirect('courses_list')
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'course_create.html', {'form': form})

# Login va register uchun viewlar
def user_login(request):
    if request.user.is_authenticated:
        return redirect('courses_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('courses_list')
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

from users.forms import RegisterForm
def user_register(request):
    if request.user.is_authenticated:
        return redirect('courses_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses_list')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})



@login_required
@require_POST
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'STUDENT':
        course.students.add(request.user)
        messages.success(request, "Siz kursga muvaffaqiyatli yozildingiz!")
    return redirect('course_detail', pk=pk)
