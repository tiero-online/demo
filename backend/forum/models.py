from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AbstractDateTimeModel(models.Model):
    """Абстрактная модель реализует время и дату создание сущностей"""
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    modified = models.DateTimeField('Дата редактирования', auto_now=True)

    class Meta:
        abstract = True


class Category(AbstractDateTimeModel):
    """Категории форума"""
    title = models.CharField('Название категории', max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Section(AbstractDateTimeModel):
    """Модель реализует разделы на форуме"""
    title = models.CharField('Название раздела', max_length=250)

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='sections',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title

    def count_topics(self):
        return self.topic.count()

    def count_messages(self):
        return Message.objects.filter(topic__section=self, deleted=False).count()


class Topic(AbstractDateTimeModel):
    """Модель реализует темы на форуме"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='forum_topic',
        null=True,
        on_delete=models.SET_NULL
    )

    section = models.ForeignKey(
        Section,
        verbose_name='Раздел',
        related_name='topic',
        on_delete=models.CASCADE
    )

    title = models.CharField('Название темы', max_length=250)
    text = models.TextField('Текст, описание темы')

    moderated = models.BooleanField('Просмотрено модератором', default=False)

    deleted = models.BooleanField('Удалено', default=False)

    private = models.BooleanField('Приватный', default=False)

    members = models.ManyToManyField(
        User,
        related_name='private_topics',
        verbose_name='Участники',
        blank=True
    )

    readers = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.private:
            if self.user not in self.members.all():
                self.members.add(self.user)

        super().save(*args, **kwargs)

    def count_messages(self):
        return self.message.count()


class Message(AbstractDateTimeModel):
    """Модель сообщений на форуме"""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='forum_message',
        null=True,
        on_delete=models.SET_NULL
    )

    topic = models.ForeignKey(
        Topic,
        verbose_name='Тема сообщения',
        related_name='message',
        on_delete=models.CASCADE
    )

    text = models.TextField('Текст сообщения')

    moderated = models.BooleanField('Просмотрено модератором', default=False)

    deleted = models.BooleanField('Удалено', default=False)

    readers = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Сообщение на форуме'
        verbose_name_plural = 'Сообщения на форуме'

    def __str__(self):
        return self.text[:20]

    def safe_delete(self):
        self.deleted = True
        self.save()


# class MinimalForumBannedUsers(models.Model):
#     """Модель, хранящая список минимально забаненныъ юзеров"""
#     blacklist = models.ManyToManyField(User, blank=True)
#
#     class Meta:
#         verbose_name = 'Минимально забаненные'
#         verbose_name_plural = verbose_name
#
#
# class MaximalForumBannedUsers(models.Model):
#     """Модель, хранящая список максимально забаненныъ юзеров"""
#     blacklist = models.ManyToManyField(User, blank=True)
#
#     class Meta:
#         verbose_name = 'Максимально забаненные'
#         verbose_name_plural = verbose_name
