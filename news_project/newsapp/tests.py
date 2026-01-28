from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from .models import Article
from publishers.models import Publisher


class ArticleAPITest(APITestCase):
    def test_subscribed_articles(self):
        user = CustomUser.objects.create(username='reader', role='reader')
        owner = CustomUser.objects.create(username='owner', role='editor')
        publisher = Publisher.objects.create(name='Test Publisher', owner=owner)
        article = Article.objects.create(
            title='Test',
            author=user,
            publisher=publisher,
            status='published',
            is_approved=True
        )
        user.subscribed_publishers.add(publisher)
        url = reverse('newsapp:subscribed-articles', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
