from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.section.views import SectionAPIView, PosterAPIView, CategoryViewSet, ParsingGymAPIView

router = DefaultRouter()
router.register('poster', PosterAPIView)
router.register('category', CategoryViewSet)
router.register('', SectionAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('gyms/', ParsingGymAPIView.as_view())
]
