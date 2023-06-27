import uuid

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

    def activate(self):
        self.is_active = True
        self.save()

    def generate_activation_token(self):
        token = uuid.uuid4()
        ActivateUserToken.objects.create(token=token, user=self)
        return token


class ActivateUserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=36, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.email

    def delete_token(self):
        self.__class__.objects.filter(user=self.user).delete()
