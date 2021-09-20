from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, mixins

from backend.forum.models import (
    Category, Section, Topic, Message,
)

from .serializers import (
    DynamicCategorySerializer,
    DynamicSectionSerializer,
    DynamicTopicSerializer,
    DynamicMessageSerializer
)

from backend.forum.permissions import (
    IsModerator,
    CanWriteComments, CanCreateTopics, HaveAccessToForum
)

from backend.utils.decorators import permissions as perms
from backend.utils.mixins import DynamicModelSerializersMixin


# Категории на форуме


class Categories(DynamicModelSerializersMixin, generics.ListAPIView):
    """Вывод всех категорий"""
    permission_classes = [permissions.AllowAny, HaveAccessToForum]
    queryset = Category.objects.all()
    serializer_class = DynamicCategorySerializer
    serializer_exclude = ('created', 'modified')


#  Разделы на форуме


class Sections(DynamicModelSerializersMixin, generics.ListAPIView):
    """Просмотр всех разделов"""
    permission_classes = [permissions.AllowAny, HaveAccessToForum]
    queryset = Section.objects.order_by('title')
    serializer_class = DynamicSectionSerializer
    serializer_fields = ('id', 'title')


#  Топики (темы) на форуме


class ReadAndCreateTopics(APIView):
    """Просмотр и создание топиков"""
    permission_classes = [permissions.AllowAny, HaveAccessToForum]

    @staticmethod
    def get(request):
        """Вывод всех топиков раздела"""
        section_pk = request.GET.get('pk', None)

        if not section_pk:
            return Response('Нет pk')

        section = Section.objects.get(id=section_pk)
        section_serializer = DynamicSectionSerializer(
            section,
            fields=(
                'id',
                'title',
                'count_topics',
                'count_messages'
            )
        )

        topics = Topic.objects.filter(section=section, deleted=False, private=False)
        serializer = DynamicTopicSerializer(
            topics,
            fields=(
                'title',
                'user',
                'section',
                'text',
                'count_messages',
                'id'
            ),
            many=True
        )

        return Response({'section': section_serializer.data,
                         'topics': serializer.data})

    @perms(permissions.IsAuthenticated, CanCreateTopics)
    def post(self, request):
        """Создание нового топика"""
        serializer = DynamicTopicSerializer(
            data=request.data,
            fields=(
                'id',
                'section',
                'title',
                'text'
            )
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class ChangeTopics(APIView):
#     """Изменение и удаление топиков"""
#     permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
#
#     # @perms(CanEditTopics)
#     def patch(self, request):
#         """Изменение топика"""
#         pk = request.data.get('pk')
#         instance = Topic.objects.get(id=pk)
#
#         if instance.user != request.user and request.user.profile.is_forum_moderator is not True:
#             return Response('Нельзя редактировать чужую тему', status=403)
#         elif request.user.profile.is_forum_moderator:
#             if (
#                     0 not in request.user.moderator_rights.rights.all()
#             ) or (
#                     4 not in request.user.moderator_rights.rights.all()
#             ):
#                 return Response('Нет прав', status=403)
#
#         serializer = DynamicTopicSerializer(
#             instance=instance,
#             data=request.data,
#             fields=(
#                 'id',
#                 'section',
#                 'title',
#                 'text'
#             )
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=400)
#
#     # @perms(CanDeleteTopics)
#     def delete(self, request):
#         pk = request.data.get('pk')
#         instance = Topic.objects.get(id=pk)
#
#         if instance.user != request.user and request.user.profile.is_forum_moderator is not True:
#             return Response('Нельзя удалить чужую тему', status=403)
#         elif request.user.profile.is_forum_moderator:
#             if (
#                     0 not in request.user.moderator_rights.rights.all()
#             ) or (
#                     5 not in request.user.moderator_rights.rights.all()
#             ):
#                 return Response('Нет прав', status=403)
#
#         instance.deleted = True
#         instance.save()
#
#         return Response('Удалено')


class ChangeTopics(DynamicModelSerializersMixin, mixins.DestroyModelMixin, generics.UpdateAPIView):
    """Изменение и удаление топиков"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    queryset = Topic.objects.all()
    serializer_class = DynamicTopicSerializer
    serializer_fields = ('id', 'section', 'title', 'text')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {'id': self.request.data.get('pk')}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_destroy(self, instance):
        instance.safe_delete()


#  Сообщения (комментарии) на форуме


class ReadAndCreateMessages(APIView):
    permission_classes = [permissions.AllowAny, HaveAccessToForum]

    @staticmethod
    def get(request):
        """Вывод всех сообщений топика"""
        topic_pk = request.GET.get('pk', None)

        if not topic_pk:
            return Response('Нет pk')

        topic = Topic.objects.get(id=topic_pk)

        if topic.private and request.user not in topic.members.all():
            return Response('Это приватная тема, вы не входите в состав участников', status=403)

        topic_serializer = DynamicTopicSerializer(topic)

        comments = Message.objects.filter(topic_id=topic_pk, deleted=False)
        serializer = DynamicMessageSerializer(
            comments,
            exclude=('topic',),
            many=True
        )

        return Response({'topic': topic_serializer.data,
                         'comments': serializer.data})

    @perms(permissions.IsAuthenticated, CanWriteComments)
    def post(self, request):
        """Написание нового сообщения"""
        serializer = DynamicMessageSerializer(
            data=request.data,
            fields=(
                'topic',
                'text'
            )
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChangeMessages(APIView):
    """Изменение и удаление сообщений на форуме"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]

    @staticmethod
    def patch(request):
        """Изменение сообщения"""
        pk = request.data.get('pk')
        instance = Message.objects.get(id=pk)

        if instance.user != request.user:
            return Response('Нельзя редактировать чужое сообщение', status=403)

        serializer = DynamicMessageSerializer(
            instance=instance,
            data=request.data,
            fields=(
                'topic',
                'text'
            )
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @staticmethod
    def delete(request):
        """Фейковое удаление сообщения"""
        pk = request.data.get('pk')
        instance = Message.objects.get(id=pk)

        if instance.user != request.user and request.user.profile.is_forum_moderator is not True:
            return Response('Нельзя удалить чужое сообщение', status=403)
        elif request.user.profile.is_forum_moderator:
            if (
                    0 not in request.user.moderator_rights.rights.all()
            ) or (
                    6 not in request.user.moderator_rights.rights.all()
            ):
                return Response('Нет прав', status=403)

        instance.deleted = True
        instance.save()

        return Response('Удалено')


class MyTopics(generics.ListAPIView):
    """
    Все топики, создателем которых является текущий юзер
    и которые не удалены
    """
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    serializer_class = DynamicTopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user, deleted=False)


class MyMessages(generics.ListAPIView):
    """
    Все сообщения, автором которых является текущий юзер
    и которые не удалены
    """
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    serializer_class = DynamicMessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user, deleted=False)


class CountMessages(APIView):
    """Выводит количество сообщений в топике"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]

    @staticmethod
    def get(request):
        pk = request.GET.get('pk')
        time = timezone.now() - timedelta(hours=24)
        count_messages = Message.objects.filter(topic_id=pk, created__gte=time).count()
        return Response({'messages': count_messages})


class NotModeratedTopics(generics.ListAPIView):
    """Вывод немодерированных топиков"""
    permission_classes = [IsModerator]
    serializer_class = DynamicTopicSerializer

    def get_queryset(self):
        pk = self.request.GET.get('pk', None)
        if pk:
            return Topic.objects.filter(section_id=pk, moderated=False)
        return Topic.objects.filter(moderated=False)


class NotModeratedMessages(generics.ListAPIView):
    """Вывод немодерированных сообщений"""
    permission_classes = [IsModerator]
    serializer_class = DynamicMessageSerializer

    def get_queryset(self):
        pk = self.request.GET.get('pk', None)
        if pk:
            return Message.objects.filter(topic_id=pk, moderated=False)
        return Message.objects.filter(moderated=False)


class ModerateTopics(APIView):
    """Помечаются модерированными топики"""
    permission_classes = [IsModerator]

    @staticmethod
    def post(request):
        list_id = request.data.get('list_id', [])
        updated = Topic.objects.filter(id__in=list_id).update(moderated=True)
        return Response({'list': list_id, 'result': updated})


class ModerateMessages(APIView):
    """Помечаются модерированными сообщения"""
    permission_classes = [IsModerator]

    @staticmethod
    def post(request):
        list_id = request.data.get('list_id', [])
        updated = Message.objects.filter(id__in=list_id).update(moderated=True)
        return Response({'list': list_id, 'result': updated})


class NewMessages(generics.ListAPIView):
    """Вывод новых сообщений в топике"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    serializer_class = DynamicMessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            topic_id=self.request.GET.get('pk')
        ).exclude(
            readers=self.request.user
        )


class NewTopics(generics.ListAPIView):
    """Вывод новых топиков"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    serializer_class = DynamicTopicSerializer

    def get_queryset(self):
        pk = self.request.GET.get('pk', None)
        if pk:
            return Topic.objects.filter(section_id=pk).exclude(readers=self.request.user)
        return Topic.objects.exclude(readers=self.request.user)


class SearchTopics(DynamicModelSerializersMixin, generics.ListAPIView):
    """Поиск тем форума"""
    permission_classes = [permissions.IsAuthenticated, HaveAccessToForum]
    serializer_class = DynamicTopicSerializer
    serializer_fields = ('id', 'title', 'user')

    def get_queryset(self):
        key = self.request.GET.get('key', None)
        return Topic.objects.filter(deleted=False, title__iexact=key)
