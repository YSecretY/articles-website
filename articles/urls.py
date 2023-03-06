from django.urls import path
from .views import (
    ArticleCreateAPIView,
    ArticlesListAPIView,
    ArticleDetailAPIView,
    ArticleUpdateAPIView,
    DateTimeAPIView,
)

urlpatterns = [
    path('create/', ArticleCreateAPIView.as_view(), name='article_create'),
    path('list/', ArticlesListAPIView.as_view(), name='articles_list'),
    path('detail/<int:pk>/', ArticleDetailAPIView.as_view(), name='article_detail'),
    path('update/<int:pk>/', ArticleUpdateAPIView.as_view(), name='article_update'),
    path('datetime/', DateTimeAPIView.as_view(), name='datetime')
]
