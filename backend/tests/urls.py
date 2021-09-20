# coding=utf-8
from django.urls import path
from backend.tests import views

urlpatterns = [
    path('categories/', views.AllCategories.as_view()),
    path('tests/', views.TestsInCategory.as_view()),
    path('questions/', views.QuestionsInTest.as_view()),
    path('answers/', views.AnswersInQuestion.as_view()),
    path('complete/', views.CompleteQuestion.as_view()),

]
