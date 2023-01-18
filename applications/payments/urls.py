from rest_framework.routers import DefaultRouter

from applications.payments.views import SubscriptionViewSet, MakeSubscriptionView

router = DefaultRouter()

router.register('payment', MakeSubscriptionView)
router.register('', SubscriptionViewSet)

urlpatterns = router.urls