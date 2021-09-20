# coding=utf-8
from django.urls import path
from backend.forum import views

urlpatterns = [
    path('', views.Categories.as_view()),

    path('sections/', views.Sections.as_view()),

    path('topic/', views.ReadAndCreateTopics.as_view()),
    # path('topic/create/', views.CreateTopic.as_view()),
    path('topic/change/', views.ChangeTopics.as_view()),
    path('topic/my/', views.MyTopics.as_view()),
    path('topic/comments/', views.CountMessages.as_view()),
    path('topic/not_moderated/', views.NotModeratedTopics.as_view()),
    path('topic/moderate/', views.ModerateTopics.as_view()),
    path('topic/new/', views.NewTopics.as_view()),

    path('comments/', views.ReadAndCreateMessages.as_view()),
    path('comments/change/', views.ChangeMessages.as_view()),
    path('comments/my/', views.MyMessages.as_view()),
    path('comments/not_moderated/', views.NotModeratedMessages.as_view()),
    path('comments/new/', views.NewMessages.as_view()),

    # path('ban/minimal/', views.MinimalBan.as_view()),
    # path('ban/maximal/', views.MaximalBan.as_view()),

    path('search/', views.SearchTopics.as_view()),

    # path('comments/add/', views.CreateMessage.as_view()),

]
