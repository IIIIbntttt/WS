from django.urls import path
from .views import ProductListView, RegisterAPIView

urlpatterns = [
    path('products', ProductListView().as_view()),
    path('signup', RegisterAPIView.as_view())
]