from django.urls import path
from .views import (
    ArticleCreateAPIView,
    ArticlesListAPIView,
)

urlpatterns = [
    path('create/', ArticleCreateAPIView.as_view(), name='article_create'),
    path('list/', ArticlesListAPIView.as_view(), name='articles_list'),
]
