from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SectionAPIView, PosterAPIView

router = DefaultRouter()
router.register('poster', PosterAPIView)
router.register('', SectionAPIView)

urlpatterns = [
    path('', include(router.urls))
]