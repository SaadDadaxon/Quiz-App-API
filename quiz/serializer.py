from rest_framework import serializers
from .models import Category, Question, Answers, Result


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class MiniAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('id', 'answer', 'create_date')


class QuestionGETSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'questions')


class QuestionSerializer(serializers.ModelSerializer):
    answers = MiniAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'category', 'questions', 'answers', 'create_date')


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ('id', 'author', 'category', 'result', 'create_date')




