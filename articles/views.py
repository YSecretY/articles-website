from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article
from .serializers import ArticleSerializer

from users.models import User

from django.shortcuts import get_object_or_404

from datetime import datetime

import json


class ArticlesListAPIView(APIView):
    queryset = Article.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleUpdateAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        """Allows only the author of the article change it"""
        article = get_object_or_404(Article, pk=pk)
        if article.author.pk != request.user.id:
            return Response('Not author of this article.', status=status.HTTP_403_FORBIDDEN)

        serializer = ArticleSerializer(article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'content': request.data.get('content'),
            'time_created': request.data.get('time_created'),
            'author': request.data.get('author')
        }
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DateTimeAPIView(APIView):
    """APIView that return current date and time in JSON"""
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        now = datetime.now()
        json_data = json.dumps(now, default=str)
        return Response(json_data.split('"')[1], status=status.HTTP_200_OK)
