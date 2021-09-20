from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    """Модель отзыва"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reviews',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    name = models.CharField('Имя пользователя', max_length=50)
    text = models.TextField('Текст отзыва', max_length=1500)
    social_link = models.URLField('Ссылка на соц. сеть')
    git_link = models.URLField('Ссылка на гит')

    moderated = models.BooleanField('Модерировано', default=False)

    def __str__(self):
        return self.name
