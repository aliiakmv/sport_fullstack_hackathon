from rest_framework import mixins
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.section.models import Section, Poster
from applications.section.permission import IsOwner
from applications.section.serializers import SectionSerializer, SectionListSerializer, PosterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import logging

logger = logging.getLogger('main')

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SectionListAPIView(ListAPIView):
    logger.info('section_list')
    queryset = Section.objects.all()
    serializer_class = SectionListSerializer


class SectionAPIView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    logger.info('section')
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsOwner]
    pagination_class = [LargeResultsSetPagination]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user)


class PosterAPIView(ModelViewSet):
    logger.info('poster')
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = [IsAdminUser]

