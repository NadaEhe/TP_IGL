# from rest_framework.test import APITestCase, APIRequestFactory
# # from .views import PostListCreateView
# from django.urls import reverse
# from rest_framework import status
# # from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
# from base.models import User



# # User = get_user_model()


# class TestUserCreation(APITestCase):
#     client = APIClient()

#     def setUp(self):
#         response = self.client.post(reverse("register") , data = {
#              "username":'testuser', "email":'testuser@example.com', "password":'secret'
#         })
#         print(response)
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # assert returned data is valid
#         self.assertEqual(response.data['title'], 'new annonce')
#         # self.assertEqual(response.data['description'], 'new description')


#     def testUserCreation(self):
#         user = User.objects.get(username = "testuser")
#         self.assertEqual(user.username , 'new annonce')

#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)




#     # def test_annonces(self):
#     #     response = self.client.get(reverse("search"))

#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     # self.assertEqual(response.data["message"], "Hello World")

