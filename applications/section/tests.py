from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from applications.section.models import Category, Section
from applications.section.views import SectionAPIView, CategoryViewSet, PosterAPIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class CategoryTest(APITestCase):
    """
    Test category view
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_user()

    @staticmethod
    def setup_user():
        return User.objects.create_user('test@gmail.com', '1', is_active=True)

    @staticmethod
    def setup_category():
        list_of_category = [
            Category('category1'),
            Category('category2'),
            Category('category3'),
        ]
        Category.objects.bulk_create(list_of_category)

    def test_get_category(self):
        request = self.factory.get('/api/v1/sport_sections/category/')
        view = CategoryViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        assert Category.objects.count() == 3
        assert Category.objects.first().title == 'category1'

    def test_post_category(self):
        data = {
            'title': 'test'
        }
        request = self.factory.post('/api/v1/sport_sections/category/', data)
        force_authenticate(request, user=self.user)
        view = CategoryViewSet.as_view({'post': 'create'})

        response = view(request)
        assert response.status_code == 201
        assert Category.objects.filter(title='test').exists()


class SectionTest(APITestCase):
    """
    Test product view
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.setup_category()
        self.user = self.setup_trainer()
        self.access_token = self.setup_trainer_token()

    @staticmethod
    def setup_trainer():
        return User.objects.create_superuser('test@gmail.com', '1')

    def setup_trainer_token(self):
        data = {
            'email': 'test@gmail.com',
            'password': '1'
        }
        request = self.factory.post('/api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()

        response = view(request)
        return response.data['access']

    @staticmethod
    def setup_category():
        Category.objects.create(title='test_product')

    def test_post_section(self):
        image = open('media/images/Screenshot_from_2022-12-12_17-10-23.png', 'rb')
        data = {
            'category': Category.objects.first().title,
            'title': 'test_post',
            'price': 20,
            'address': 'test',
            'description': 'test',
            'images': image
        }
        request = self.factory.post('/api/v1/sport_sections/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        view = SectionAPIView.as_view({'post': 'create'})
        image.close()
        response = view(request)
        print(response.data)

        assert response.status_code == 201
        assert Section.objects.filter(title='test_post').exists()

    def test_get_section(self):
        request = self.factory.get('/api/v1/sport_sections/')
        view = SectionAPIView.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200


class PosterTest(APITestCase):
    """
    Test poster view
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setup_superuser()
        self.access_token = self.setup_superuser_token()

    @staticmethod
    def setup_superuser():
        return User.objects.create_superuser('test@gmail.com', '1')

    def setup_superuser_token(self):
        data = {
            'email': 'test@gmail.com',
            'password': '1'
        }
        request = self.factory.post('/api/v1/account/login/', data)
        view = TokenObtainPairView.as_view()

        response = view(request)
        return response.data['access']

    def test_post_poster(self):
        image = open('media/images/Screenshot_from_2022-12-12_17-10-23.png', 'rb')
        data = {
            'image': image
        }
        request = self.factory.post('/api/v1/sport_sections/poster/', data, HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        view = PosterAPIView.as_view({'post': 'create'})
        image.close()
        response = view(request)
        print(response.data)

        assert response.status_code == 201
