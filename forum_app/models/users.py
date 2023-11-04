from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Meta:
        unique_together = ('email',)

    def __str__(self):
        return self.username
