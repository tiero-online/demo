from django.contrib import admin

from .models import Category, Course, Task, RealizationTask
from backend.utils.admin import all_fields

from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий"""
    list_display = ('title',)


class CourseAdmin(SummernoteModelAdmin):
    """Админка курсов"""
    list_display = all_fields(
        Course, 'image', 'height', 'width', 'id',
        'description', 'program', 'target_audience',
        'requirements'
    )
    list_display.append('term')
    list_display.append('count_seats')
    readonly_fields = ('count_tasks',)


class TaskAdmin(admin.ModelAdmin):
    """Админка заданий"""
    list_display = all_fields(Task, 'id')


class RealizationTaskAdmin(admin.ModelAdmin):
    """Админка выполнения заданий"""
    list_display = all_fields(RealizationTask)
    list_editable = ("success",)
    readonly_fields = ('answer',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(RealizationTask, RealizationTaskAdmin)
