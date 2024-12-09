from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя пользователя', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', blank=False, unique=True)
    email = models.CharField(max_length=254, verbose_name='Почта', blank=False, unique=True)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)

    def __str__(self):
        return self.username