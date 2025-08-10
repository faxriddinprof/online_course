from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Category, Section
from courses.forms import CourseForm, ModuleForm, SectionForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



@login_required(login_url='login_student_html')
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


@login_required
def course_detail(request, pk, section_id=None, module_id=None):
    course = get_object_or_404(Course, pk=pk)
    sections = course.sections.all().prefetch_related('modules')

    section = None
    module = None

    # Agar section_id bo'lmasa — birinchi bo‘lim
    if section_id:
        section = get_object_or_404(course.sections, id=section_id)
    elif sections.exists():
        section = sections.first()

    # Agar module_id bo'lmasa — birinchi modul
    if section:
        if module_id:
            module = get_object_or_404(section.modules, id=module_id)
        elif section.modules.exists():
            module = section.modules.first()

    return render(request, 'course_detail.html', {
        'course': course,
        'sections': sections,
        'current_section': section,
        'current_module': module,
    })



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
            return redirect('section-create', course_id=course.id)  # yangi
    else:
        form = CourseForm()
    return render(request, 'course-create/course_create.html', {'form': form})

@login_required
@require_POST
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'STUDENT':
        course.students.add(request.user)
        messages.success(request, "Siz kursga muvaffaqiyatli yozildingiz!")
    return redirect('course_detail', pk=pk)


@login_required
def section_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.author:
        messages.error(request, "Siz faqat o'zingiz yaratgan kursga bo'lim qo'sha olasiz.")
        return redirect('courses_list')

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            return redirect('module-create', section_id=section.id)
    else:
        form = SectionForm()

    return render(request, 'course-create/section_create.html', {'form': form, 'course': course})


@login_required
def module_create(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.user != section.course.author:
        messages.error(request, "Siz faqat o'zingiz yaratgan kursga modul qo'sha olasiz.")
        return redirect('courses_list')

    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            module.section = section
            module.save()
            messages.success(request, "Modul qo'shildi.")
            return redirect('courses_list')
    else:
        form = ModuleForm()

    return render(request, 'course-create/module_create.html', {'form': form, 'section': section})
