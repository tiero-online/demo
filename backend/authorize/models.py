from django.db import models
from django.conf import settings


class EmailChangeKey(models.Model):
    """Модель для смены email, хранит ключ подтверждения"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    key = models.CharField('Ключ подтверждения смены email', max_length=42)
    new_email = models.EmailField('Новый email')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            from backend.utils.send_mail import generate
            self.key = generate(length=42)
        super(EmailChangeKey, self).save(*args, **kwargs)
