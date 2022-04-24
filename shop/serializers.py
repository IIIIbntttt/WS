from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


