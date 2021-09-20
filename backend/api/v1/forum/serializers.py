from django.contrib.auth.models import User

from rest_framework import serializers

from backend.profile.serializers import DynamicProfileSerializer
from backend.forum.models import Category, Section, Topic, Message

from backend.utils.serializers import DynamicFieldsModelSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализация профиля юзера"""
    profile = DynamicProfileSerializer(fields=('id', 'username', 'image'))

    class Meta:
        model = User
        fields = ('profile',)


class DynamicSectionSerializer(DynamicFieldsModelSerializer):
    """Динамический сериализер раздела форума"""
    class Meta:
        model = Section
        fields = '__all__'


class DynamicCategorySerializer(DynamicFieldsModelSerializer):
    """Динамический сериализер категории форума"""
    sections = DynamicSectionSerializer(
        fields=(
            'id',
            'title',
            'count_topics',
            'count_messages'
        ),
        many=True
    )

    class Meta:
        model = Category
        fields = '__all__'

# class SectionSerializer(serializers.ModelSerializer):
#     """Частичная сериализация раздела форума"""
#     class Meta:
#         model = Section
#         fields = ('id', 'title', 'count_topics', 'count_messages')


# class MinSectionSerializer(serializers.ModelSerializer):
#     """Минимальная сериализация раздела форума"""
#     class Meta:
#         model = Section
#         fields = ('id', 'title')


class DynamicTopicSerializer(DynamicFieldsModelSerializer):
    """Полная сериализация темы форума"""
    user = UserProfileSerializer()

    class Meta:
        model = Topic
        fields = '__all__'


# class TopicSerializer(serializers.ModelSerializer):
#     """Частичная сериализация темы форума"""
#     user = UserProfileSerializer()
#
#     class Meta:
#         model = Topic
#         fields = ('title', 'user', 'section', 'text', 'count_messages', 'id')


# class SearchTopicSerializer(serializers.ModelSerializer):
#     """Сериализация топиков в поиске"""
#     user = UserProfileSerializer()
#
#     class Meta:
#         model = Topic
#         fields = ('id', 'title', 'user')


# class CreateTopicSerializer(serializers.ModelSerializer):
#     """Сериализер для создания тем на форуме"""
#     class Meta:
#         model = Topic
#         fields = ('id', 'section', 'title', 'text')


class DynamicMessageSerializer(DynamicFieldsModelSerializer):
    """Полная сериализация сообщения на форуме"""
    user = UserProfileSerializer()
    topic = DynamicTopicSerializer()

    class Meta:
        model = Message
        fields = '__all__'


# class MessageSerializer(serializers.ModelSerializer):
#     """Частичная сериализация сообщения на форуме"""
#     user = UserProfileSerializer()
#
#     class Meta:
#         model = Message
#         exclude = ('topic', )


# class CreateMessageSerializer(serializers.ModelSerializer):
#     """Сериализер для создания сообщений на форуме"""
#     class Meta:
#         model = Message
#         fields = ('topic', 'text')


class CategorySerializer(serializers.ModelSerializer):
    """Частичная сериализация категории форума"""
    sections = DynamicSectionSerializer(
        fields=(
            'id',
            'title',
            'count_topics',
            'count_messages'
        ),
        many=True
    )

    class Meta:
        model = Category
        exclude = ('created', 'modified')
