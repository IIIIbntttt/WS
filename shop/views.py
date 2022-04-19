from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, permissions
from .renderers import CustomRenderer
from rest_framework.response import Response
from shop.serializers import UserSerializer, GroupSerializer, ProductListSerializer
from rest_framework import generics
from .models import Product
import json


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    renderer_classes = [CustomRenderer]

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def post(self, request, *args, **kwargs):
        data = json.load(request)
        p = Product(
            name=data['name'],
            description=data['description'],
            price=data['price']
        )
        p.save()
        return Response(data={"id": p.id, "message": "Product added"}, status=status.HHTP_204_NO_CONTENT)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    renderer_classes = [CustomRenderer]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
