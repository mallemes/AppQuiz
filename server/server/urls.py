from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from quiz_app.views import IndexView, RegisterViewAPI, UserLogin, UserLogout, QuizViewSet
from server import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/alpha/register/', RegisterViewAPI.as_view(), name='api_register'),
    path('api/alpha/login/', UserLogin.as_view(), name='api_login'),
    path('api/alpha/logout/', UserLogout.as_view(), name='api_logout'),
    path('api/alpha/quiz/', QuizViewSet.as_view({"get": "list"})),
    # path('api/alpha/setcsrf/', SetCSRFCookie.as_view()),
    path('api/alpha/quiz/<int:pk>', QuizViewSet.as_view({"get": "retrieve"})),
    # path('api/alpha/quiz/', CreateQuizAPI.as_view(), name='api_create_quiz'),
    path('', IndexView.as_view()),
    path('quiz/', include('quiz_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
