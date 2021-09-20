# coding=utf-8
from django.urls import path
from backend.courses import views

urlpatterns = [
    path('list/', views.CategoryList.as_view()),
    path('category/', views.CoursesInCategory.as_view()),
    path('my/', views.MyCourses.as_view()),
    path('', views.CourseTasks.as_view()),
    path('task/', views.Tasks.as_view()),
    path('buy/', views.BuyCourse.as_view()),
    path('description/', views.CourseDescription.as_view()),
    # path('next/', views.CompletedTasks.as_view()),

]
