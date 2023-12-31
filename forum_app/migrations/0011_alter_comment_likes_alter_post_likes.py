# Generated by Django 4.2.5 on 2023-09-21 18:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0010_remove_comment_likes_comment_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
    ]
