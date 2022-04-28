from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    username = None
    fio = models.CharField(max_length=255, blank=False, verbose_name="Фамилия, Имя, Отчество")
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False, validators=[MinLengthValidator(6)])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return self.name
