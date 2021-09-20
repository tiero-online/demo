from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from backend.utils.models import AbstractImageModel
from backend.tests.models import Test

User = settings.AUTH_USER_MODEL


class Category(AbstractImageModel):
    """Модель категорий"""
    title = models.CharField('Категория', max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Course(AbstractImageModel):
    """ Класс модели курсов"""
    title = models.CharField('Название курса', max_length=100)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='courses',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    description = models.TextField('Описание курса', max_length=5000)
    program = models.TextField('Программа курса', max_length=5000, null=True)
    target_audience = models.TextField('Целевая аудитория', max_length=5000, null=True)
    requirements = models.TextField('Требования', max_length=5000, null=True)
    price = models.IntegerField('Стоимость курса')
    date_start = models.DateField('Дата начала курса')
    date_end = models.DateField('Дата окончания курса')
    students = models.ManyToManyField(
        User,
        blank=True,
        verbose_name='Учащиеся',
        related_name='courses'
    )
    instructor = models.ForeignKey(
        User,
        verbose_name='Преподаватель',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='my_courses'
    )
    count_tasks = models.PositiveIntegerField('Количество заданий', default=0)

    available = models.IntegerField('Количество мест', default=0)

    is_active = models.BooleanField('Активный', default=False)

    lessons_on_weak = models.PositiveIntegerField('Количество занятий в неделю', default=0)

    lessons_time = models.CharField(
        'Время проведения занятий',
        max_length=500,
        null=True,
        blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title

    def term(self):
        return self.date_end - self.date_start
    term.short_description = 'Длительность курса'

    def count_seats(self):
        return self.available - self.students.count()
    count_seats.short_description = 'Свободно мест'

    def count_students(self):
        return self.students.count()
    count_students.short_description = 'Количество учеников'


class Task(models.Model):
    """ Класс модели задания курса"""
    course = models.ForeignKey(
        Course,
        verbose_name='Курс',
        related_name='tasks',
        on_delete=models.CASCADE)
    title = models.CharField('Название задания', max_length=50)
    description = models.TextField('Описание задания', max_length=3000)
    date_start = models.DateTimeField('Дата начала выполнения задания')
    date_end = models.DateTimeField('Дата окончания выполнения задания')
    # questions = models.ManyToManyField(
    #     Question,
    #     verbose_name='Задания',
    #     related_name='tasks',
    #     blank=True
    # )
    test = models.ForeignKey(
        Test,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Тест',
        related_name='tasks'
    )

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title


@receiver(post_save, sender=Task)
def plus_count_tasks(instance, created, **kwargs):
    """Прибавление 1 к счетчику заданий в курсе"""
    if created:
        instance.course.count_tasks += 1
        instance.course.save()


@receiver(post_delete, sender=Task)
def minus_count_tasks(instance, **kwargs):
    """Убавление 1 от счетчика заданий в курсе"""
    instance.course.count_tasks -= 1
    instance.course.save()


class RealizationTask(models.Model):
    """Модель исполнения задания"""
    task = models.ForeignKey(
        Task,
        verbose_name='Выполнение',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    student = models.ForeignKey(
        User,
        verbose_name='Ученик',
        on_delete=models.CASCADE
    )
    answer = models.TextField('Ответ', max_length=1000)
    comment = models.TextField(
        'Комментарий преподавателя',
        max_length=1500,
        blank=True
    )
    success = models.BooleanField('Выполнено', default=False)
    date_create = models.DateTimeField('Дата сдачи', auto_now_add=True)

    class Meta:
        verbose_name = 'Выполненное задание'
        verbose_name_plural = 'Выполненные задания'

    def __str__(self):
        return self.task.title
