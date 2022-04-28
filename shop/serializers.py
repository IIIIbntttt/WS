from rest_framework import serializers
from .models import Article
from shop.models import User


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

