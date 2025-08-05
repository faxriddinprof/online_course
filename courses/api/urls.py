from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView,
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    SectionListCreateView, SectionDetailView,
    ModuleListCreateView, ModuleDetailView,
    PublicCourseListView, PublicCourseDetailView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),

    path('', PublicCourseListView.as_view(), name='public-course-list'),
    path('<int:pk>/', PublicCourseDetailView.as_view(), name='public-course-detail'),

    path('my/', CourseListView.as_view(), name='course-list'),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),

    path('<int:course_id>/sections/', SectionListCreateView.as_view(), name='section-list-create'),
    path('sections/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),

    path('sections/<int:section_id>/modules/', ModuleListCreateView.as_view(), name='module-list-create'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
]