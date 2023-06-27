from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('Email address', unique=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
