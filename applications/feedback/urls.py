from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.feedback.views import FavoriteAPIView, ReviewAPIView, RatingAPIView, LikeAPIView

router = DefaultRouter()
router.register('favorite', FavoriteAPIView)
router.register('review', ReviewAPIView)
router.register('rating', RatingAPIView)
router.register('like', LikeAPIView)

urlpatterns = [
    path('', include(router.urls))
]
