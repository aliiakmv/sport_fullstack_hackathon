from django.shortcuts import render

# Create your views here.
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import mixins, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from feedback.models import Rating, Like
from feedback.serializers import RatingSerializer
from .models import Section, Poster
from .permission import IsOwner
from .serializers import SectionSerializer, PosterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
import logging

logger = logging.getLogger('main')


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SectionAPIView(ModelViewSet):
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
