# from rest_framework import serializers

from backend.profile.models import UserProfile
from backend.courses.serializers import MinimalCourseSerializer

from backend.utils.serializers import DynamicFieldsModelSerializer


class DynamicProfileSerializer(DynamicFieldsModelSerializer):
    """
    Сериализер профиля с динамическими полями,
    которые указываются параметром 'fields',
    """
    completed_courses = MinimalCourseSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


# class ProfileSerializer(serializers.ModelSerializer):
#     """Сериализация профиля юзера"""
#     completed_courses = MinimalCourseSerializer(many=True)
#
#     class Meta:
#         model = UserProfile
#         fields = ('username', 'email', 'image', 'completed_courses')
#
#
# class EditProfileSerializer(serializers.ModelSerializer):
#     """Сериализация изменения профиля юзера"""
#     class Meta:
#         model = UserProfile
#         fields = ('image',)
        # fields = ('username', 'email', 'image', 'completed_courses')


# class ForumProfileSerializer(serializers.ModelSerializer):
#     """Сериализация профиля юзера для форума"""
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'username', 'image')
