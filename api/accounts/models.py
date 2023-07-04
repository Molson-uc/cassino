from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)

    is_bank = models.BooleanField(default=False)
    is_gamemaster = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
