from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from server.quiz_app.models import Quiz


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
