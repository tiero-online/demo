# Generated by Django 2.1 on 2018-10-16 08:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions_count', models.PositiveIntegerField(default=0, editable=False)),
                ('counter', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PossibleAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Вариант')),
                ('is_right', models.BooleanField(default=False, verbose_name='Является верным ответом')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответа',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150, verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='TestCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория тестов',
                'verbose_name_plural': 'Категории тестов',
            },
        ),
        migrations.AddField(
            model_name='test',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tests', to='tests.TestCategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tests.Test', verbose_name='Тест'),
        ),
        migrations.AddField(
            model_name='possibleanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tests.Question', verbose_name='Вопрос'),
        ),
        migrations.AddField(
            model_name='answerscounter',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counter', to='tests.Test', verbose_name='Тест'),
        ),
        migrations.AddField(
            model_name='answerscounter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers_counter', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
