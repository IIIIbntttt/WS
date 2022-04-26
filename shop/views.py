from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .renderers import CustomRenderer
from rest_framework import response, status, permissions
from .serializers import ArticleSerializer, RegisterSerializer
from rest_framework import generics
from .models import Product, User
import json


class RegisterAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductListView(generics.ListCreateAPIView):
#     serializer_class = ProductListSerializer
#     renderer_classes = [CustomRenderer]
#
#     def get_queryset(self):
#         products = Product.objects.all()
#         return products
#
#     def post(self, request, *args, **kwargs):
#         data = json.load(request)
#         p = Product(
#             name=data['name'],
#             description=data['description'],
#             price=data['price']
#         )
#         p.save()
#         return Response(data={"id": p.id, "message": "Product added"}, status=status.HHTP_204_NO_CONTENT)


class ArticlesListView(generics.ListAPIView):  # ListAPIView Используется только для чтения: GET
    """Вывод списка продуктов"""
    permission_classes = [permissions.AllowAny]
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]
    queryset = Product.objects.all()  # Набор записей с которыми мы рабAотаем в этой view


class ArticleCreateView(generics.CreateAPIView):
    """Создание продукта"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):  # RetrieveUpdateDestroyAPIView -
    """Вывод отдельного продукта"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer]
