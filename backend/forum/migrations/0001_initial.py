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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('title', models.CharField(max_length=250, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='MaximalForumBannedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blacklist', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('moderated', models.BooleanField(default=False, verbose_name='Просмотрено модератором')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('readers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение на форуме',
                'verbose_name_plural': 'Сообщения на форуме',
            },
        ),
        migrations.CreateModel(
            name='MinimalForumBannedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blacklist', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('title', models.CharField(max_length=250, verbose_name='Название раздела')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sections', to='forum.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('title', models.CharField(max_length=250, verbose_name='Название темы')),
                ('text', models.TextField(verbose_name='Текст, описание темы')),
                ('moderated', models.BooleanField(default=False, verbose_name='Просмотрено модератором')),
                ('deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('private', models.BooleanField(default=False, verbose_name='Приватный')),
                ('members', models.ManyToManyField(blank=True, related_name='private_topics', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
                ('readers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='forum.Section', verbose_name='Раздел')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_topic', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='forum.Topic', verbose_name='Тема сообщения'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_message', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
