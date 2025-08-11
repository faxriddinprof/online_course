from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Course

@login_required
def profile_view(request):
    return render(request, 'profils/profile.html')

@login_required
def my_courses_view(request):
    if request.user.role == 'STUDENT':
        courses = request.user.enrolled_courses.all()
    elif request.user.role == 'TEACHER':
        courses = request.user.courses.all()
    else:
        courses = []
    return render(request, 'profils/my_courses.html', {'courses': courses})
