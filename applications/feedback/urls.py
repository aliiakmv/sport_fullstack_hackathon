from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.feedback.views import ReviewAPIView

router = DefaultRouter()
router.register('review', ReviewAPIView)

urlpatterns = [
    path('', include(router.urls))
]
