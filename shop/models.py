
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    fio = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    last_login = models.DateTimeField(auto_now=True)


    # @property
    # def token(self):
    #     token = jwt.encode(
    #         {'username': self.fio, 'email': self.email,
    #             'exp': datetime.utcnow() + timedelta(hours=24)},
    #         settings.SECRET_KEY, algorithm='HS256')
    #
    #     return


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()

