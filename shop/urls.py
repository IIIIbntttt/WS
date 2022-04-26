from django.urls import path
from .views import ArticleDetailView, RegisterAPIView, ArticlesListView

urlpatterns = [
    path('articles', ArticlesListView().as_view()),
    path('signup', RegisterAPIView.as_view()),
    # path('product', ProductListView().as_view())
]
