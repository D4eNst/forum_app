from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    text = HTMLField(max_length=3000, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views_cnt = models.IntegerField(default=0, editable=False, verbose_name='Просмотры')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активный')

    views = models.ManyToManyField('CustomUser', verbose_name="Просмотры", related_name="viewed_posts", blank=True)
    likes = models.ManyToManyField('CustomUser', verbose_name="Лайки", related_name="liked_posts", blank=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория', db_index=True)
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, verbose_name='Автор', null=True, db_index=True)

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at', 'title', ]

