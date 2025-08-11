

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include('users.api.urls')),
    path('users/', include('users.urls')),
    path('', include('courses.urls')),
    path('api/courses/', include('courses.api.urls')),
    path('profils/', include('profils.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
