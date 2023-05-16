from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import Quiz, Answer, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "textAnswer", "isCorrect"]


class QuestionSerializer(serializers.ModelSerializer):
    answer_set = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "questionText", "quiz", "answer_set"]


class QuizSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "name", "created_at", "author", "question_set"]

    # def create(self, validated_data):
    #     print(validated_data)
    #     pass
    #     # question_set = validated_data.pop('question_set')
    #     # quiz = super().create(validated_data)
    #     # for child in question_set:
    #     #     child['quiz'] = quiz
    #     # self.fields['question_set'].create(question_set)
    #     # return quiz


class QuizSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "name", "created_at", "author"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True,
                                      validators=[validate_password])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password1'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user



