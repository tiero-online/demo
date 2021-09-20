# Generated by Django 2.1 on 2018-10-16 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import backend.utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(editable=False, null=True)),
                ('width', models.IntegerField(editable=False, null=True)),
                ('image', models.ImageField(blank=True, height_field='height', null=True, upload_to=backend.utils.models.create_path, verbose_name='Изображение', width_field='width')),
                ('title', models.CharField(max_length=50, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(editable=False, null=True)),
                ('width', models.IntegerField(editable=False, null=True)),
                ('image', models.ImageField(blank=True, height_field='height', null=True, upload_to=backend.utils.models.create_path, verbose_name='Изображение', width_field='width')),
                ('title', models.CharField(max_length=100, verbose_name='Название курса')),
                ('description', models.TextField(max_length=5000, verbose_name='Описание курса')),
                ('program', models.TextField(max_length=5000, null=True, verbose_name='Программа курса')),
                ('target_audience', models.TextField(max_length=5000, null=True, verbose_name='Целевая аудитория')),
                ('requirements', models.TextField(max_length=5000, null=True, verbose_name='Требования')),
                ('price', models.IntegerField(verbose_name='Стоимость курса')),
                ('date_start', models.DateField(verbose_name='Дата начала курса')),
                ('date_end', models.DateField(verbose_name='Дата окончания курса')),
                ('count_tasks', models.PositiveIntegerField(default=0, verbose_name='Количество заданий')),
                ('available', models.IntegerField(default=0, verbose_name='Количество мест')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('lessons_on_weak', models.PositiveIntegerField(default=0, verbose_name='Количество занятий в неделю')),
                ('lessons_time', models.CharField(blank=True, max_length=500, null=True, verbose_name='Время проведения занятий')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='courses.Category', verbose_name='Категория')),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_courses', to=settings.AUTH_USER_MODEL, verbose_name='Преподаватель')),
                ('students', models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL, verbose_name='Учащиеся')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='RealizationTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(max_length=1000, verbose_name='Ответ')),
                ('comment', models.TextField(blank=True, max_length=1500, verbose_name='Комментарий преподавателя')),
                ('success', models.BooleanField(default=False, verbose_name='Выполнено')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата сдачи')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Выполненное задание',
                'verbose_name_plural': 'Выполненные задания',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название задания')),
                ('description', models.TextField(max_length=3000, verbose_name='Описание задания')),
                ('date_start', models.DateTimeField(verbose_name='Дата начала выполнения задания')),
                ('date_end', models.DateTimeField(verbose_name='Дата окончания выполнения задания')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='courses.Course', verbose_name='Курс')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='tests.Test', verbose_name='Тест')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.AddField(
            model_name='realizationtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.Task', verbose_name='Выполнение'),
        ),
    ]
