from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Category, Section
from courses.forms import CourseForm, ModuleForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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

    # Foydalanuvchi ushbu kursga yozilganmi?
    is_enrolled = request.user in course.students.all()

    section = None
    module = None

    if section_id:
        section = get_object_or_404(course.sections, id=section_id)
    elif sections.exists():
        section = sections.first()

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
        'is_enrolled': is_enrolled,
    })


@login_required
def course_content(request, pk, section_id=None, module_id=None):
    course = get_object_or_404(Course, pk=pk)
    # Foydalanuvchi yozilganligini tekshirish
    if request.user not in course.students.all():
        messages.error(request, "Kurs kontentini ko'rish uchun kursga yozilish kerak.")
        return redirect('course_detail', pk=pk)

    sections = course.sections.all().prefetch_related('modules')

    section = None
    module = None

    if section_id:
        section = get_object_or_404(course.sections, id=section_id)
    elif sections.exists():
        section = sections.first()

    if section:
        if module_id:
            module = section.modules.filter(id=module_id).first()
        elif section.modules.exists():
            module = section.modules.first()

    return render(request, 'course_content.html', {
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
        return redirect('course_content', pk=pk)  # Kurs kontent sahifasiga yo'naltirish
    return redirect('course_detail', pk=pk)


@login_required
def section_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.author:
        messages.error(request, "Siz faqat o'zingiz yaratgan kursga bo'lim qo'sha olasiz.")
        return redirect('courses_list')

    if request.method == 'POST':
        titles = request.POST.getlist('titles[]')
        for title in titles:
            if title.strip():
                Section.objects.create(course=course, title=title.strip())
        messages.success(request, f"{len(titles)} ta bo'lim qo'shildi.")
        return redirect('module-create', section_id=course.sections.first().id)

    return render(request, 'course-create/section_create.html', {'course': course})


@login_required
def module_create(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    course = section.course

    # Foydalanuvchi muallifligini tekshirish
    if request.user != course.author:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Ruxsat yo‘q'}, status=403)
        return redirect('courses_list')

    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        sec_id = request.POST.get('section_id')
        sec = get_object_or_404(Section, id=sec_id, course=course)

        if form.is_valid():
            module = form.save(commit=False)
            module.section = sec
            module.save()

            # ✅ Xabar qo‘shish
            messages.success(request, f"✅ '{module.title}' nomli modul muvaffaqiyatli qo‘shildi!")

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                modules = list(sec.modules.values('id', 'title'))
                return JsonResponse({
                    'success': True,
                    'modules': modules,
                    'message': f"✅ '{module.title}' nomli modul muvaffaqiyatli qo‘shildi!"
                })

            return redirect('module-create', section_id=sec.id)

        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    else:
        form = ModuleForm()

    return render(request, 'course-create/module_create.html', {
        'form': form,
        'section': section,
        'course': course
    })
