from rest_framework import serializers

from server.quiz_app.models import Quiz, Answer


class QuizSerializer(serializers.ModelSerializer):
    model = Quiz

    class Meta:
        fields = ["questionText", "created_at"]


class AnswerSerializer(serializers.ModelSerializer):
    model = Answer
