from rest_framework.viewsets import ModelViewSet

from applications.payments.models import Customer, Subscription
from applications.payments.permissions import IsSubscriptionOwner
from applications.payments.serializers import SubscriptionSerializer, CustomerSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionOfferViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriptionOwner]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
