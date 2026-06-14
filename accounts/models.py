from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.USER
    )
