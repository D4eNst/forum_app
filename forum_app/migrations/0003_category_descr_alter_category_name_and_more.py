# Generated by Django 4.2.5 on 2023-09-08 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descr',
            field=models.TextField(max_length=500, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=60, verbose_name='URL'),
        ),
    ]
