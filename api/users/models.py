from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from api.core.models import BaseModelMixin


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=190)

    last_name = models.CharField(max_length=190, null=True, blank=True)
    objects = BaseUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'users'
