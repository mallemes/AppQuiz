from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=250)
    poster = models.ImageField(null=True, blank=True)
    author = models.CharField(null=True, blank=True, max_length=250)  # author
    users = models.ManyToManyField(User, through="Competition")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('show_quiz', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Question(models.Model):
    questionText = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.questionText


class Answer(models.Model):
    textAnswer = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isCorrect = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.textAnswer + str(self.isCorrect)


class Competition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    point = models.PositiveSmallIntegerField(null=True, blank=True)
    total = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
