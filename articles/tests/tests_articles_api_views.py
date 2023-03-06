from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from articles.models import Article

from rest_framework_simplejwt.tokens import AccessToken


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

    def test_articles_list_view(self):
        self.client.logout()

        response = self.client.get(reverse('articles_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')

    def test_article_create_view_for_logged_in_users(self):
        access_token = AccessToken.for_user(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {
            'title': 'Django',
            'description': 'Article about django',
            'content': 'This is the hole text of the article',
            'author': self.user.id
        }
        response = self.client.post(reverse('article_create'), data=data, **headers)
        self.assertEqual(response.status_code, 201)

    def test_article_create_view_for_logged_out_users(self):
        self.client.logout()

        data = {
            'title': 'Django',
            'description': 'Article about django',
            'content': 'This is the hole text of the article',
            'author': self.user.id
        }
        response = self.client.post(reverse('article_create'), data=data)
        self.assertEqual(response.status_code, 401)

    def test_article_detail_view_for_logged_in_users(self):
        access_token = AccessToken.for_user(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        response = self.client.get(reverse('article_detail', args=[self.article.pk]), **headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertContains(response, 'Short story from Harry Potter')

    def test_article_detail_view_for_logged_out_users(self):
        self.client.logout()

        response = self.client.get(reverse('article_detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 401)

    def test_article_update_view_for_logged_in_users(self):
        access_token = AccessToken.for_user(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {
            'title': 'Harry Potter (updated)',
            'description': 'Short story from Harry Potter (updated)',
            'content': 'This is the hole content of the article (updated)',
            'author': self.user.id
        }
        response = self.client.put(
            reverse('article_update', args=[self.article.pk]),
            data=data, **headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'updated')
        self.assertEqual(response.data['author'], self.user.id)

    def test_article_update_view_for_wrong_authenticated_user(self):
        new_user = get_user_model().objects.create_user(
            name='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )
        access_token = AccessToken.for_user(new_user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        data = {
            'title': 'Harry Potter (updated by new user)',
            'description': 'Short story from Harry Potter (updated by new user)',
            'content': 'This is the hole content of the article (updated by new user)',
            'author': self.user.id
        }
        response = self.client.put(
            reverse('article_update', args=[self.article.pk]),
            data=data,
            **headers,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_article_update_view_for_logged_out_users(self):
        self.client.logout()

        response = self.client.put(reverse('article_update', args=[self.article.pk]))

        self.assertEqual(response.status_code, 401)

    def test_article_delete_view_for_logged_in_users(self):
        access_token = AccessToken.for_user(self.user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        response = self.client.delete(reverse('article_delete', args=[self.article.pk]), **headers)

        self.assertEqual(response.status_code, 204)

    def test_article_delete_view_for_logged_in_wrong_users(self):
        new_user = get_user_model().objects.create_user(
            name='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )
        access_token = AccessToken.for_user(new_user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        response = self.client.delete(reverse('article_delete', args=[self.article.pk]), **headers)

        self.assertEqual(response.status_code, 403)

    def test_article_delete_view_for_admin(self):
        new_user = get_user_model().objects.create_user(
            name='testuser1',
            email='testuser1@email.com',
            password='testpass123',
            is_staff='True'
        )
        access_token = AccessToken.for_user(new_user)
        headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}

        response = self.client.delete(reverse('article_delete', args=[self.article.pk]), **headers)

        self.assertEqual(response.status_code, 204)

    def test_article_delete_view_for_logged_out_users(self):
        self.client.logout()

        response = self.client.delete(reverse('article_delete', args=[self.article.pk]))

        self.assertEqual(response.status_code, 401)
