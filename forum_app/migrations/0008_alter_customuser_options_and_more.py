# Generated by Django 4.2.5 on 2023-09-16 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0007_comment_created_at_comment_likes_comment_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together={('email',)},
        ),
    ]
