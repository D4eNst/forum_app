# Generated by Django 4.2.5 on 2023-10-24 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_app', '0015_useractivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя события')),
            ],
        ),
    ]
