from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Article


class ArticleTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='testuser',
            email='testuser@email.com',
            password='testpass123'
        )

        self.article = Article.objects.create(
            title='Harry Potter',
            description='Short story from Harry Potter',
            content='This is the hole content of the article',
            author=self.user
        )

    def test_article_list_view_for_logged_out_users(self):
        self.client.logout()
        response = self.client.get(reverse('articles_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')

    def test_article_create_view_for_logged_in_users(self):
        data = {
            'title': 'Django',
            'description': 'Article about django',
            'content': 'This is the hole text of the article',
            'author': self.user.id
        }
        response = self.client.post(reverse('article_create'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get(reverse('articles_list'))
        # FIXME: Should check particularly detail view of this article, not the list of them
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the hole text of the article')
