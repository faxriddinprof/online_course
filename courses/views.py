from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Category, Section, ModuleProgress, Module
from courses.forms import CourseForm, ModuleForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Prefetch



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
    return render(request, 'course/courses_list.html', {
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

    return render(request, 'course/course_detail.html', {
        'course': course,
        'sections': sections,
        'current_section': section,
        'current_module': module,
        'is_enrolled': is_enrolled,
    })



@login_required
def course_create(request):
    if not request.user.role == 'TEACHER':
        return redirect('course/courses_list')
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

    # ❌ Agar foydalanuvchi kurs muallifi bo‘lsa yozila olmaydi
    if request.user == course.author:
        messages.error(request, "Siz o'zingiz yaratgan kursga yozila olmaysiz.")
        return redirect('course_detail', pk=pk)

    # ✅ Kursga yozilish (rolidan qat'i nazar)
    course.students.add(request.user)
    messages.success(request, "Siz kursga muvaffaqiyatli yozildingiz!")

    return redirect('course_content', pk=pk)


@login_required
def section_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.author:
        messages.error(request, "Siz faqat o'zingiz yaratgan kursga bo'lim qo'sha olasiz.")
        return redirect('course/courses_list')

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
        return redirect('course/courses_list')

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
    
@login_required
def teacher_students(request):
    if request.user.role != 'TEACHER':
        messages.error(request, "Faqat o‘qituvchilar uchun ruxsat etilgan.")
        return redirect('courses_list')

    # Faqat shu o‘qituvchining kurslari + o‘quvchilari
    teacher_courses = Course.objects.filter(author=request.user).prefetch_related('students')

    return render(request, 'statistics_for_teacher/teacher_students.html', {
        'teacher_courses': teacher_courses
    })





@login_required
def course_content(request, pk, section_id=None, module_id=None):
    course = get_object_or_404(Course, pk=pk)

    if request.user not in course.students.all():
        messages.error(request, "Kurs kontentini ko'rish uchun kursga yozilish kerak.")
        return redirect('course_detail', pk=pk)

    # Bo'lim va modullarni tartib bilan oling
    sections_qs = course.sections.order_by('id')
    sections = sections_qs.prefetch_related(
        Prefetch('modules', queryset=Module.objects.order_by('id'))
    )

    # Hozirgi bo'lim
    if section_id:
        section = get_object_or_404(sections_qs, id=section_id)
    else:
        section = sections_qs.first()

    # Hozirgi modul
    if section is None:
        # kursda bo'limlar yo'q bo'lsa
        return render(request, 'course/course_content.html', {
            'course': course, 'sections': sections, 'current_section': None, 'current_module': None,
            'completed_modules': [], 'next_url': reverse('courses_list'), 'next_label': 'Kursni yakunlash',
        })

    if module_id:
        module = get_object_or_404(Module, id=module_id, section=section)
    else:
        module = section.modules.order_by('id').first()


     # ✅ Foydalanuvchi progressi
    completed_modules = list(
        ModuleProgress.objects.filter(user=request.user, completed=True).values_list('module_id', flat=True)
    )

    # ✅ Har bir bo‘lim uchun progress foizi
    section_progress = {}
    for sec in sections:
        total = sec.modules.count()
        done = sum(1 for m in sec.modules.all() if m.id in completed_modules)
        percent = int((done / total) * 100) if total > 0 else 0
        section_progress[sec.id] = percent




    # Progress (agar modelingiz bo‘lmasa, keyingi 2 qatorni [] qilib yuboring)
    completed_modules = list(
        ModuleProgress.objects.filter(user=request.user, completed=True).values_list('module_id', flat=True)
    ) if 'ModuleProgress' in globals() else []

    # Keyingi tugma hisob-kitobi
    sections_list = list(sections_qs)  # bo'limlar ketma-keti
    current_sec_index = next((i for i, s in enumerate(sections_list) if s.id == section.id), 0)

    modules_list = list(section.modules.order_by('id'))
    current_mod_index = next((i for i, m in enumerate(modules_list) if m.id == module.id), 0)

    if current_mod_index + 1 < len(modules_list):
        # Bo'lim ichidagi keyingi modul
        next_mod = modules_list[current_mod_index + 1]
        next_url = reverse('course_content_module', args=[course.id, section.id, next_mod.id])
        next_label = 'Davom etish'
    else:
        # Bo'lim tugadi → keyingi bo'lim bormi?
        if current_sec_index + 1 < len(sections_list):
            next_sec = sections_list[current_sec_index + 1]
            next_mod = next_sec.modules.order_by('id').first()
            if next_mod:
                next_url = reverse('course_content_module', args=[course.id, next_sec.id, next_mod.id])
            else:
                next_url = reverse('course_content_section', args=[course.id, next_sec.id])
            next_label = 'Bo‘limni yakunlash'
        else:
            # Kurs tugadi
            next_url = reverse('courses_list')
            next_label = 'Kursni yakunlash'

    return render(request, 'course/course_content.html', {
        'course': course,
        'sections': sections,
        'current_section': section,
        'current_module': module,
        'completed_modules': completed_modules,
        'section_progress': section_progress,  # ✅ qo‘shildi
        'next_url': next_url,
        'next_label': next_label,
    })
