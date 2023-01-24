from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.feedback.models import Rating, Like
from applications.feedback.serializers import RatingSerializer
from applications.section.models import Section, Poster, Category, ParsingGym
from applications.section.permission import IsOwner
from applications.section.section_recommendations_mixin import RecommendationMixin
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
class SectionAPIView(RecommendationMixin, ModelViewSet):
    logger.info('section')
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):
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

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(section_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


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


