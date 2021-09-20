from django.test import TestCase

# Create your tests here.

# from .models import Course, RealizationTask
#
#
# class OpenedTasks:
#     def get(self, request):
#         course_pk = request.GET.get('course_pk')
#         course = Course.objects.get(id=course_pk)
#         tasks = course.tasks.all()
#         completed_tasks = RealizationTask.objects.filter(
#             student=request.user, success=True, task__in=tasks)
#         c
