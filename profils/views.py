from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileEditForm
from courses.models import Course

@login_required
def profile_view(request):
    return render(request, 'profils/profile.html')

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi!")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'profils/edit_profile.html', {'form': form})

@login_required
def my_courses(request):
    if request.user.role == 'STUDENT':
        courses = request.user.enrolled_courses.all()
    else:
        courses = Course.objects.filter(author=request.user)
    return render(request, 'profils/my_courses.html', {'courses': courses})
