import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from .user_manager import UserManager


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} ({self.email})"

