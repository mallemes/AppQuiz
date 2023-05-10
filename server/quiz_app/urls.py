from django.urls import path

from server.quiz_app.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('show/<int:pk>', QuizShowView.as_view(), name="show")
    # path('auth/register/', Register.as_view(), name="myRegister"),
    # path('auth/login/', LoginUser.as_view(), name="myLogin"),
    # path('auth/logout/', my_user_logout, name="myLogout"),
]
