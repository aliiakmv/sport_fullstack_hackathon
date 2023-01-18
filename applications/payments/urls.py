from rest_framework.routers import DefaultRouter

from applications.payments.views import CustomerViewSet, SubscriptionOfferViewSet

router = DefaultRouter()

router.register('customer_profile', CustomerViewSet)
router.register('', SubscriptionOfferViewSet)

urlpatterns = router.urls
