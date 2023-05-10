from django.contrib.auth.models import User
from django.db import models


# class MyUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    name = models.CharField(max_length=250)
    poster = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    questionText = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    textAnswer = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isCorrect = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
