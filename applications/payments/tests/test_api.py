import json
import token
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from model_bakery import baker

from django.contrib.auth import get_user_model

from applications.payments.models import Customer
from applications.payments.views import SubscriptionOfferViewSet
from applications.section.models import Section, Category
from applications.section.views import SectionAPIView

User = get_user_model()


class SubscribeAPITestCase(APITestCase):
    """Тестирование представлений абонемента"""
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_superuser('customer@gmail.com', 'clouds22')
        self.user .save()
        self.access_token = self.setup_user_token()
        self.customer = self.setup_customer()
        self.customer.save()
        self.section = self.setup_sport_section()
        self.section.save()

    def setup_customer(self):
        return Customer.objects.create(user=self.user, phone='0555001090', card_number='4485818557975555', card_type='visa',
                                card_expiry_date='2024-01-03', card_balance=10000)

    def setup_user_token(self):
        response = self.client.post('/api/v1/account/login/',
                                    {'email': 'customer@gmail.com', 'password': 'clouds22'})
        content = json.loads(response.content)
        return content['access']

    def setup_sport_section(self):
        test_trainer = User.objects.create_superuser(email='trainer@gmail.com', password='0')
        test_category = Category.objects.create(title='test_sports_category')
        list_of_sections = baker.make('section.Section', category=test_category, trainer=test_trainer, price=5000)
        return list_of_sections

    def buy_subscription(self):
        new_data = {
            'classes': self.section.id,
            'customer': self.customer.id,
            'type': 'visa'
        }
        response = self.client.post(reverse('subscriptions-list'), new_data,
                                    HTTP_AUTHORIZATION=f'Bearer {self.access_token}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
