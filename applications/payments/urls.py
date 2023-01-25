from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.payments.views import CustomerViewSet, SubscriptionOfferViewSet, SubscriptionViewSet

router = DefaultRouter()

router.register('customer_profile', CustomerViewSet, basename='profile')
router.register('', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('pay/<uuid:subscription_key>/', SubscriptionOfferViewSet.as_view())
]
urlpatterns += router.urls
