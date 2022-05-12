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


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.TextField(validators=[MinLengthValidator(3)])
    order_price = models.IntegerField()
