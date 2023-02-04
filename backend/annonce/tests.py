from rest_framework.test import APITestCase, APIRequestFactory
# from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
# from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from base.models import User
from .models import Annonce



# User = get_user_model()


class TestAnnonceCreation(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='secret'
        )

        # create annonce
        self.annonce = Annonce.objects.create(
            author=self.user, title='test annonce',
            description='test description', category='test category',
            theme='test theme', surface=10,
            sold=10, wilaya='test wilaya', commune='test commune'
        )
    def testCreation(self):
        annonce = Annonce.objects.get(title = 'test annonce')
        self.assertEqual(annonce.author.email, 'testuser@example.com')
        self.assertEqual(annonce.description, 'test description')
        self.assertEqual(annonce.category, 'test category')
        self.assertEqual(annonce.theme, 'test theme')
        self.assertEqual(annonce.surface, 10)
        self.assertEqual(annonce.sold, 10)
        self.assertEqual(annonce.wilaya, 'test wilaya')
        self.assertEqual(annonce.commune, 'test commune')

    def testGetAnnonces(self):
        self.client.login(email='testuser@example.com', password='secret')
        response = self.client.get(reverse('annonces'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'test annonce')
        self.assertEqual(response.data[0]['description'], 'test description')
    
    def testCreateFavorite(self):
        annonce = Annonce.objects.get(title = 'test annonce')
        user = User.objects.get(email = 'testuser@example.com')

        response = self.client.post(reverse("create_favorite") , data={"user" : user.id, "annonce" : annonce.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
