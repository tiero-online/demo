from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов"""
    class Meta:
        model = Review
        fields = ('name', 'text', 'social_link', 'git_link')
