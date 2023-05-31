from django.contrib.sites.shortcuts import get_current_site
from django.urls import path, reverse
from . import views


urlpatterns = [
    path('category-list/', views.CategoryList.as_view()),
    path('question-list/<int:category_id>/', views.QuestionList.as_view()),
    path('answer-student/', views.AnswerStudent.as_view()),
    # path('answer-student/<int:category_id>/question/<int:questions_id>/answer/<int:answers_id>/', views.AnswerStudentUrls.as_view()),
    # path('month-static/', views.MonthStatic.as_view()),
    # path('week-static/', views.WeekStatic.as_view()),
    # path('day-static/', views.DayStatic.as_view()),
    path('result-average-category/', views.ResultList.as_view()),
    path('result-average-account/', views.ResultListAccount.as_view()),
    path('daily-statistics/', views.CategoryStatisticsAPIView.as_view()),  # """ ?category_id=1&start_date=2023-05-27 """   Example
]



