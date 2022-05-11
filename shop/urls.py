from django.urls import path
from .views import *

urlpatterns = [
    path('articles', ArticlesListView().as_view()),
    path('signup', RegisterView.as_view()),
    path('article', ArticleCreateView().as_view()),
    path('article/<int:pk>', ArticleDetailView().as_view()),
    path('login', CustomAuthToken().as_view()),
    path('logout', Logout.as_view()),
]
