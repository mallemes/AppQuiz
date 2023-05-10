from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from server.server import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
