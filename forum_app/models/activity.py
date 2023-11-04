from django.db import models
from forum_app.models import CustomUser, Post


class ActivityName(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя события")
    def __str__(self):
        return f'{self.name}'


class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    action_type = models.CharField(max_length=50, verbose_name="Тип события")
    action_name = models.ForeignKey(ActivityName, on_delete=models.CASCADE, verbose_name="Имя события")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата события")

    def __str__(self):
        return f'{self.action_type} "{self.post.title}"'



