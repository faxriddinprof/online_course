from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, Section, Module, ModuleProgress


# ========== Inline Models ==========
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ("title", "video", "youtube_url", "description")
    show_change_link = True


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    show_change_link = True


# ========== Admin Models ==========
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at", "student_count", "image_preview")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "author__username", "category__name")
    readonly_fields = ("created_at", "image_preview")
    ordering = ("-created_at",)
    inlines = [SectionInline]

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Students"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:70px; height:40px; border-radius:5px; object-fit:cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    search_fields = ("title", "course__title")
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "course_title", "video_link", "youtube_link")
    search_fields = ("title", "section__title", "section__course__title")
    list_filter = ("section__course__category",)

    def course_title(self, obj):
        return obj.section.course.title
    course_title.short_description = "Course"

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{}" target="_blank">🎬 Video</a>', obj.video.url)
        return "—"
    video_link.short_description = "Video"

    def youtube_link(self, obj):
        if obj.youtube_url:
            return format_html('<a href="{}" target="_blank">▶ YouTube</a>', obj.youtube_url)
        return "—"
    youtube_link.short_description = "YouTube"


@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "completed", "viewed_at")
    list_filter = ("completed", "viewed_at")
    search_fields = ("user__username", "module__title", "module__section__course__title")
    ordering = ("-viewed_at",)
