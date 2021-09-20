# coding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoriesList.as_view()),
    path("post-list/", views.PostList.as_view()),
    path("post-single/", views.PostSingle.as_view())
]
