from django.contrib import admin
from .models import Category, Question, Answers, Result


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class AnswerInline(admin.TabularInline):
    model = Answers
    extra = 1


@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'is_true', 'create_date')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (AnswerInline, )
    list_display = ('id', 'category', 'questions', 'create_date')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'result', 'create_date')





