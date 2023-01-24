from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteAPIView, ReviewAPIView

router = DefaultRouter()
router.register('favorite', FavoriteAPIView)
router.register('review', ReviewAPIView)

urlpatterns = [
    path('', include(router.urls))
]