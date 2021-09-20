from rest_framework import serializers
from backend.profile.serializers import DynamicProfileSerializer
from .models import Post, Category, Tag, Comments


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация категорий"""
    class Meta:
        model = Category
        fields = ("id", "name")


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов"""
    class Meta:
        model = Tag
        fields = ("id", "tag")


class PostSerializer(serializers.ModelSerializer):
    """Сериализация статей"""
    category = CategorySerializer()
    tag = TagSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ("id",
                  "title",
                  "mini_text",
                  "image",
                  "created_date",
                  "category",
                  "tag",
                  "viewed")


class PostSingleSerializer(serializers.ModelSerializer):
    """Сериализация поста"""
    category = CategorySerializer()
    tag = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ("author",
                  "title",
                  "text",
                  "published_date",
                  "image",
                  "category",
                  "tag")


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализация комментариев к статье"""
    user = DynamicProfileSerializer(fields=('id', 'username', 'image'))

    class Meta:
        model = Comments
        fields = ("id", "user", "text", "date", "update")


class CommentsPostSerializer(serializers.ModelSerializer):
    """Добавление комментариев к статье"""

    class Meta:
        model = Comments
        fields = ("text", "post")

class CommentsPUTSerializer(serializers.ModelSerializer):
    """Изменение комментариев к статье"""

    class Meta:
        model = Comments
        fields = ("id", "text", "post")