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


class DynamicTopicSerializer(DynamicFieldsModelSerializer):
    """Полная сериализация темы форума"""
    user = UserProfileSerializer()

    class Meta:
        model = Topic
        fields = '__all__'


class DynamicMessageSerializer(DynamicFieldsModelSerializer):
    """Полная сериализация сообщения на форуме"""
    user = UserProfileSerializer()
    topic = DynamicTopicSerializer()

    class Meta:
        model = Message
        fields = '__all__'
