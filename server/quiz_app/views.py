from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView

from .forms import RegisterForm
from .models import Quiz, Question, Answer, Competition


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
        myIstruees = []
        if text_question_list is not None and text_answer_list is not None and isTrueList is not None and name_quiz:
            count = 4
            myIstruees.append(int(isTrueList[0]))
            for i in range(1, len(isTrueList)):
                myIstruees.append(int(isTrueList[i]) + count)
                count += 4
            quiz = Quiz(name=name_quiz, author=author)
            quiz.save()
            sum = 0
            for i in range(0, len(text_question_list)):
                que = Question(questionText=text_question_list[i], quiz=quiz)
                que.save()
                for j in range(sum, sum + 4):
                    if myIstruees[i] - 1 == j:
                        ans = Answer(question=que, textAnswer=text_answer_list[j], isCorrect=True)
                        ans.question = que
                        ans.textAnswer = text_answer_list[j]
                        ans.isCorrect = True
                        ans.save()
                    else:
                        ans = Answer()
                        ans.question = que
                        ans.textAnswer = text_answer_list[j]
                        ans.isCorrect = False
                        ans.save()
                sum = sum + 4

        return redirect('index')
        # 'name_quiz': ['quiz1'],
        # 'poster': [''],
        # 'text_question[]': ['Qazaqstan astanasy', 'question2'],
        # 'text_answer[]': ['1text', '2text', '3text', '4text', 'answer2 - 1', 'answer2 - 2', 'answer2 - 3', 'answer2 - 4'],
        # 'isTrue[]': ['1 ', '2']}>


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
