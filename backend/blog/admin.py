from django.contrib import admin
from .models import Post, Category, Tag, Comments
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    """Статьи"""
    text = ('content',)
    list_display = ('title', 'created_date', "category")

class CommentsAdmin(admin.ModelAdmin):
    """Коментарии к статьям"""
    list_display = ("user", "post", "date", "update")

admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Category)
admin.site.register(Tag)
