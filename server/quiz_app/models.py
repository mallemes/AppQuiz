from django.db import models


# class Quiz(models.Model):
#     name = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    questionText = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    answer = models.CharField(max_length=250)
    question = models.ForeignKey(Quiz, on_delete=models.RESTRICT)
