# coding=utf-8
from django.urls import path
from backend.api.v2.forum import views

urlpatterns = [
    # v2
    path('', views.Categories.as_view()),

    path('sections/', views.Sections.as_view()),

    # path('topic/', views.ReadAndCreateTopics.as_view()),
    path('topic/change/', views.ChangeTopics.as_view()),
    path('topic/my/', views.MyTopics.as_view()),
    # path('topic/comments/', views.CountMessages.as_view()),
    path('topic/not_moderated/', views.NotModeratedTopics.as_view()),
    # path('topic/moderate/', views.ModerateTopics.as_view()),
    path('topic/new/', views.NewTopics.as_view()),

    # path('comments/', views.ReadAndCreateMessages.as_view()),
    # path('comments/change/', views.ChangeMessages.as_view()),
    path('comments/my/', views.MyMessages.as_view()),
    path('comments/not_moderated/', views.NotModeratedMessages.as_view()),
    path('comments/new/', views.NewMessages.as_view()),

    path('search/', views.SearchTopics.as_view()),

]
