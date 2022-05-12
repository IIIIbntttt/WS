from django.urls import path
from .views import *

urlpatterns = [
    path('products', ProductsListView().as_view()),
    path('signup', RegisterView.as_view()),
    path('product', ProductsCreateView().as_view()),
    path('product/<int:pk>', ProductsDetailView().as_view()),
    path('login', CustomAuthToken().as_view()),
    path('logout', Logout.as_view()),
    path('cart/<int:pk>', CartCreateDeleteView.as_view()),
    path('cart', CartListView.as_view()),
    path('order', OrderCreateView.as_view()),
]
