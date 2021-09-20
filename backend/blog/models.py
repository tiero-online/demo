from django.db import models
from django.utils import timezone
from djoser.urls.base import User


class Category(models.Model):
    """ Класс модели категорий сетей
    """
    name = models.CharField("Категория", max_length=50)
    active = models.BooleanField("Отображать?", default=True)
    parent_category = models.ForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ Класс модели тегов
    """
    tag = models.CharField("Тег", max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag


class Post(models.Model):
    """ Класс модели поста
    """
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE)
    title = models.CharField("Тема", max_length=500)
    mini_text = models.TextField("Краткое содержание", max_length=1000)
    text = models.TextField("Полное содержание", max_length=100000)
    created_date = models.DateTimeField("Дата создания", auto_now_add=True)
    published_date = models.DateTimeField("Дата публикации", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to="blog/", blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тег", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    published = models.BooleanField("Опубликовать?", default=True)
    viewed = models.IntegerField("Просмотрено", default=0)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comments(models.Model):
    """Модель коментариев к новостям"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="Новость", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=2000)
    date = models.DateTimeField("Дата", auto_now_add=True)
    update = models.DateTimeField("Изменен", auto_now=True)
    parent_comment = models.ForeignKey(
        "self",
        verbose_name="Родительский комментарий",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return "{} - {}".format(self.user, self.post)