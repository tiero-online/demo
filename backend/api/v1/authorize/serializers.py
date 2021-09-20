from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализация юзера"""
    class Meta:
        model = User
        fields = ('id', 'username')
