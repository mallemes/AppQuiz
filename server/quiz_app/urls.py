from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('show/<int:pk>', login_required(redirect_field_name="login")(QuizShowView.as_view()), name="show_quiz"),
    path('create/', login_required(CreateQuizView.as_view()), name="create_quiz"),
    path('auth/register/', Register.as_view(), name="myRegister"),
    path('profile/', login_required(ProfileView.as_view()), name="profile"),
    path('auth/login/', LoginUser.as_view(), name="myLogin"),
    path('auth/logout/', my_user_logout, name="myLogout"),
]
