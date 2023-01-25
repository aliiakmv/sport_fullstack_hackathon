import json

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterLoginUserAPITestCase(APITestCase):

    def setUp(self):
        test_user = User.objects.create_superuser(email='test@gmail.com', password='12345')
        assert test_user

    def test_register_user(self):
        response = self.client.post('/api/v1/account/register/',
                                    {'email': 'test_user@gmail.com', 'password': 'clouds22', 'password_confirm': 'clouds22',
                                     'first_name': 'Ray', 'last_name': 'K'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post('/api/v1/account/login/',
                                    {'email': 'test@gmail.com', 'password': '12345'})
        self.assertTrue('access' in json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def login_with_wrong_password(self):
        response = self.client.post('/api/v1/account/login/',
                                    {'email': 'test@gmail.com', 'password': '11113'})
        self.assertFalse('access' in json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def login_with_wrong_email(self):
        response = self.client.post('/api/v1/account/login/',
                                    {'email': 'test1@gmail.com', 'password': '11113'})
        self.assertFalse('access' in json.loads(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
