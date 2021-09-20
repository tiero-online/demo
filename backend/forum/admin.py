from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Section, Topic, Message


class CategoryAdmin(admin.ModelAdmin):
    """Админка категорий"""
    list_display = ('title', 'id')


class SectionAdmin(admin.ModelAdmin):
    """Админка разделов"""
    list_display = ("id", "title", "category", "created", 'modified')
    list_display_links = ("title", )


class TopicAdmin(SummernoteModelAdmin):
    """Админка тем"""
    text = ('content',)
    list_display = ("id", "title", "user", "modified", 'moderated', 'deleted', 'private')
    list_display_links = ("title", )
    list_editable = ('moderated', 'deleted', 'private')


class MessageAdmin(SummernoteModelAdmin):
    """Админка сообщений"""
    text = ('content',)
    list_display = ("id", "user", "topic", 'moderated', 'deleted')
    list_display_links = ("user", )


# class TopicAdmin(admin.ModelAdmin):
#     """Админка топиков"""
#     list_display = all_fields(Topic)
#     list_editable = ('moderated', 'deleted', 'private')


admin.site.register(Category)
admin.site.register(Section, SectionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message, MessageAdmin)
