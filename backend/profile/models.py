from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from backend.courses.models import Course
from backend.moderation.models import ModeratorRights
from backend.utils.models import AbstractImageModel

User = settings.AUTH_USER_MODEL


class UserProfile(AbstractImageModel):
    """Модель профиля пользователя"""

    description = 'Профиль'

    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        related_name='profile',
        on_delete=models.CASCADE
    )
    completed_courses = models.ManyToManyField(
        Course,
        blank=True,
        verbose_name='Пройденные курсы'
    )

    username = models.CharField(max_length=50, editable=False)
    email = models.EmailField(editable=False)

    is_forum_moderator = models.BooleanField('Модератор', default=False)

    class Meta:
        verbose_name = 'Профиль пользователь'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.get_username()
        if not self.email or self.email != self.user.email:
            self.email = self.get_email()

        if self.is_forum_moderator:
            if not ModeratorRights.objects.filter(user=self.user).exists():
                ModeratorRights.objects.create(user=self.user)

        super(UserProfile, self).save(*args, **kwargs)

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_completed_courses(self):
        return self.completed_courses

    # def get_info(self):
    #     return {'username': self.username,
    #             'email': self.email,
    #             'avatar': self.image or None,
    #             'courses': self.get_completed_courses()}


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        UserProfile.objects.create(user=instance, id=instance.id)
        instance.profile.save()
