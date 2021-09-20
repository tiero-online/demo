# coding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('', views.AboutModerator.as_view()),
    path('ban/', views.BanUser.as_view()),
]
