from django.db import models


class Comment(models.Model):
    user = models.ForeignKey(to='CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь', db_index=True)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE, verbose_name='Пост', db_index=True)
    likes = models.ManyToManyField('CustomUser', verbose_name="Лайки", related_name="liked_comments", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    text = models.TextField(max_length=450, verbose_name="Текст")

    # def __str__(self):
    #     return f"Комментарий к посту {self.post[:15]}: {self.user.username}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
