from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from .models import *


def forbidden_for_you(request=None):
    return JsonResponse({"error": {"code": 403, "message": "Forbidden for you"}}, status=403)


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
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'data': {'errors': serializer.errors}})


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class Logout(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return JsonResponse({"data": {"message": "logout"}}, status=201)


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
                return Response(status=HTTP_403_FORBIDDEN, data={'data': {'errors': 'Login failed'}})
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user_token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        return Response(status=HTTP_400_BAD_REQUEST, data={'data': {'errors': serializer.errors}})


class ProductsListView(generics.ListAPIView):  # ListAPIView ???????????????????????? ???????????? ?????? ????????????: GET
    """?????????? ???????????? ??????????????????"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [CustomRenderer]  # ?????????? ?????????????? ?? ???????????????? ???? ??????A?????????? ?? ???????? view


class ProductsCreateView(generics.CreateAPIView):
    """???????????????? ????????????????"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [CustomRenderer]


class ProductsDetailView(generics.RetrieveUpdateDestroyAPIView):  # RetrieveUpdateDestroyAPIView -
    """?????????? ???????????????????? ????????????????"""
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    renderer_classes = [CustomRenderer]


class CartListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CartGetSerializer
    renderer_classes = [CartRenderer]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return forbidden_for_you()
        return Cart.objects.filter(user=self.request.user)


class CartCreateDeleteView(generics.DestroyAPIView, generics.CreateAPIView):
    renderer_classes = [CartRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = CartSerializer

    def get_queryset(self, *args, **kwargs):
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return forbidden_for_you()
        request.data['product'] = kwargs['pk']
        request.data['user'] = request.user.id
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return forbidden_for_you()
        cart_to_delete = Cart.objects.filter(id=kwargs['pk'])
        if not cart_to_delete:
            return JsonResponse({"error": {"code": 404, "message": "Not found"}}, status=404)
        elif cart_to_delete[0].user != self.request.user:
            return JsonResponse({"error": {"code": 403, "message": "Forbidden for you"}}, status=403)
        request.data['product'] = kwargs['pk']
        return self.destroy(request, *args, **kwargs)


class OrderCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer
    renderer_classes = [OrderRenderer]

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return forbidden_for_you()
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return forbidden_for_you()
        current_user = self.request.user
        current_cart = Cart.objects.filter(user=current_user)
        if not current_cart:
            return JsonResponse({"error": {"code": 422, "message": "Cart is empty"}}, status=422)
        list_products = []
        order_price = 0
        for product in current_cart:
            list_products.append(product.product_id)
            order_price += product.product.price
        request.data['user'] = current_user.id
        request.data['products'] = str(list_products)
        request.data['order_price'] = order_price
        current_cart.delete()
        return self.create(request, *args, **kwargs)
