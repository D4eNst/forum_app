from django.db import models
from django.urls import reverse

# from forum_app.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=60, unique=False, db_index=True, verbose_name='URL')
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE, verbose_name='Создатель')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_list', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]
