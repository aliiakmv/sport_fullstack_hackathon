from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.section.views import SectionAPIView, SectionListAPIView, PosterAPIView
from django.views.decorators.cache import cache_page

router = DefaultRouter()
router.register('poster', PosterAPIView)
router.register('', SectionAPIView)

urlpatterns = [
    path('list/', cache_page(500) (SectionListAPIView.as_view())),
    path('', include(router.urls))
]
