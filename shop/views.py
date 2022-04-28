from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import CustomRenderer
from rest_framework import serializers
from .serializers import ArticleSerializer
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import permissions

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fio', 'email', 'password')


class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User(**serializer.validated_data)
            # ToDo убрать строку с set_password
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'data': {'errors': serializer.errors}})


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class CustomAuthToken(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except:
                return Response(status=HTTP_400_BAD_REQUEST, data={'data': {'errors': ''}})

            if not user.check_password(serializer.validated_data['password']):
                return Response('asdasd')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user_token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        return Response(status=HTTP_400_BAD_REQUEST, data={'data': {'errors': serializer.errors}})


class ArticlesListView(generics.ListAPIView):  # ListAPIView Используется только для чтения: GET
    """Вывод списка продуктов"""
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]  # Набор записей с которыми мы рабAотаем в этой view


class ArticleCreateView(generics.CreateAPIView):
    """Создание продукта"""
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):  # RetrieveUpdateDestroyAPIView -
    """Вывод отдельного продукта"""
    permission_classes = [permissions.AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]
