from rest_framework import serializers
from .models import Product
from shop.models import User


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('fio', 'email', 'password',)

    def save(self):
        account = User(fio=self.validated_data['fio'],
                           email=self.validated_data['email'],
                           password=self.validated_data['password'])
        account.save()
        return account
