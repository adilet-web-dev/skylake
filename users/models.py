from django.db import models
from django.contrib.auth.models import AbstractUser

from .user_manager import UserManager


class User(AbstractUser):
    name = models.CharField(
        "Name",
        max_length=255,
    )
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    username = None
    first_name = None
    last_name = None

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.email})"
