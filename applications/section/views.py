from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.feedback.models import Rating, Like, Favorite
from applications.feedback.serializers import RatingSerializer, LikeSerializer, FavoriteSerializer
from applications.section.models import Section, Poster, Category, ParsingGym
from applications.section.permission import IsOwner
from applications.section.serializers import SectionSerializer, PosterSerializer, CategorySerializer, \
    ParsingGymSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
import logging

logger = logging.getLogger('main')


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


@method_decorator(cache_page(60), name='dispatch')
class SectionAPIView(ModelViewSet):
    logger.info('section')
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        try:
            like_obj, _ = Like.objects.get_or_create(section_id=pk, owner=request.user)
        except MultipleObjectsReturned:
            like_obj = Like.objects.filter(section_id=pk, owner=request.user).first()
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    @action(detail=True, methods=['GET'])
    def get_like(self, request, pk, *args, **kwargs):
        liked_gym = Like.objects.get(section=self.get_object())
        list_of_users = LikeSerializer(liked_gym)
        return Response(list_of_users.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(section_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'])
    def get_rating(self, request):
        rating = Rating.objects.get(section=self.get_object())
        list_od_ratings = RatingSerializer(rating)
        return Response(list_od_ratings.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        fav_obj, _ = Favorite.objects.get_or_create(section_id=pk, owner=request.user)
        fav_obj.is_favorite = not fav_obj.is_favorite
        fav_obj.save()
        status_ = 'saved in favorites'
        if not fav_obj.is_favorite:
            status_ = 'Removed from favorites'
        return Response({'status': status_})

    @action(detail=False, methods=['GET'])
    def get_favorites(self, request):
        course = Favorite.objects.filter(is_favorite=True, owner=request.user)
        list_of_courses = FavoriteSerializer(course, many=True)
        return Response(list_of_courses.data, status=status.HTTP_200_OK)


class PosterAPIView(ModelViewSet):
    logger.info('poster')
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ParsingGymAPIView(APIView):
    @staticmethod
    def get(request):
        gyms = ParsingGym.objects.all()
        serializer_class = ParsingGymSerializer(gyms, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)


