from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterForm
from .models import Quiz, Question, Answer, Competition
from .serializers import RegisterSerializer, UserLoginSerializer, QuizSerializer, QuizSerializer2


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['quizies'] = Quiz.objects.all()
        return context


class QuizShowView(DetailView):
    model = Quiz
    template_name = "show.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        authUser = request.user
        quiz = self.get_object()

        questions = quiz.question_set.all()
        answerIds = data.getlist(f"answerId[]")
        total = questions.count()
        score = 0
        for question in questions:
            answers = question.answer_set.all()
            for answer in answers:
                if answer.isCorrect and str(answer.id) in answerIds:
                    score += 1

        competited_quiz = Competition.objects.filter(user=authUser, quiz_id=quiz.id).first()
        if competited_quiz:
            competited_quiz.point = score
            competited_quiz.total = total
            competited_quiz.save()
        else:
            Competition.objects.create(user=authUser, quiz_id=quiz.id, point=score, total=total)

        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super(QuizShowView, self).get_context_data(**kwargs)
        context['comptdUsers'] = Competition.objects.filter(quiz=self.get_object()).all()
        return context


class CreateQuizView(TemplateView):
    template_name = "create.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        name_quiz = data.get('name_quiz')
        author = request.user
        text_question_list = data.getlist("text_question[]")
        text_answer_list = data.getlist("text_answer[]")
        isTrueList = data.getlist("isTrue[]")

        if text_question_list and text_answer_list and isTrueList and name_quiz:
            quiz = Quiz(name=name_quiz, author=author)
            quiz.save()

            for i, text_question in enumerate(text_question_list):
                que = Question(questionText=text_question, quiz=quiz)
                que.save()
                start_index = i * 4
                end_index = start_index + 4

                for j, text_answer in enumerate(text_answer_list[start_index:end_index]):
                    ans = Answer(question=que, textAnswer=text_answer, isCorrect=(j == int(isTrueList[i]) - 1))
                    ans.save()

        return redirect('index')


class Register(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy('myLogin')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        competited_quiz = Competition.objects.filter(user=self.request.user).all()
        count = []
        for i in competited_quiz:
            count.append(i.point / i.quiz.question_set.count() * 100)

        print(count)
        context["count"] = count
        context["awards"] = competited_quiz

        return context


@login_required
def my_user_logout(request):
    logout(request)
    messages.info(request, "success")
    return redirect("/")


# =======================API=======================

class RegisterViewAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# @method_decorator(csrf_protect, name="dispatch")
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            authUser = User.objects.filter(username=data.get("username")).values()
            print(authUser)
            login(request, user)
            return Response(authUser[0], status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class QuizViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        name_quiz = data.get('name_quiz')
        # name_quiz = data.get('name')
        author = request.user
        text_question_list = data.get("text_questions", [])
        text_answer_list = data.get("text_answers", [])
        isTrueList = data.get("isTrues", [])

        if text_question_list and text_answer_list and isTrueList and name_quiz:
            quiz = Quiz(name=name_quiz, author=author)
            quiz.save()

            for i, text_question in enumerate(text_question_list):
                que = Question(questionText=text_question, quiz=quiz)
                que.save()
                start_index = i * 4
                end_index = start_index + 4

                for j, text_answer in enumerate(text_answer_list[start_index:end_index]):
                    ans = Answer(question=que, textAnswer=text_answer, isCorrect=(j == isTrueList[i] - 1))
                    ans.save()

            return Response({'message': 'quiz successfully created'}, status=status.HTTP_302_FOUND)  # Redirect response
        else:
            return Response({'message': 'error invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        self.serializer_class = QuizSerializer2
        return super().list(request)
