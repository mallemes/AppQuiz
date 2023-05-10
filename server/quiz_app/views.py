from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView

from .models import Quiz, Question, Answer


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['quizies'] = Quiz.objects.all()
        return context


class QuizShowView(DetailView):
    model = Quiz
    template_name = "show.html"
    queryset = Quiz.objects.all()


class CreateQuizView(TemplateView):
    template_name = "create.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        name_quiz = data['name_quiz']
        text_question_list = data.getlist("text_question[]")
        text_answer_list = data.getlist("text_answer[]")
        isTrueList = data.getlist("isTrue[]")
        print(text_answer_list)
        print(text_question_list)
        print(isTrueList)
        myIstruees = []
        if text_question_list is not None and text_answer_list is not None and isTrueList is not None:
            count = 4
            myIstruees.append(int(isTrueList[0]))
            for i in range(1, len(isTrueList)):
                if len(isTrueList) == 1:
                    myIstruees.append(int(isTrueList[i]))
                    # return myIstruees
                else:
                    myIstruees.append(int(isTrueList[i]) + count)
                    count += 4
            print(myIstruees)
            quiz = Quiz()
            quiz.name = name_quiz
            quiz.save()
            sum = 0
            for i in range(0, len(text_question_list)):
                que = Question()
                que.questionText = text_question_list[i]
                que.quiz = quiz
                que.save()
                for j in range(sum, sum + 4):
                    if myIstruees[i] - 1 == j:
                        ans = Answer()
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
