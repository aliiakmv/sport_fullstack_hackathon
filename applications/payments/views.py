from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.payments.models import Customer, Subscription
from applications.payments.permissions import IsSubscriptionOwner
from applications.payments.serializers import SubscriptionSerializer, CustomerSerializer
from applications.section.models import Section


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriptionOwner]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset().filter(customer=self.request.user)
        return queryset


class SubscriptionOfferViewSet(APIView):

    @staticmethod
    def get(request, subscription_key):
        subscription = get_object_or_404(Subscription, subscription_key=subscription_key)
        customer = Customer.objects.filter(user=subscription.customer)[0]

        if customer.card_balance < subscription.final_price:
            return Response({'message': 'There is not enough money on your card'}, status=status.HTTP_400_BAD_REQUEST)

        customer.card_balance = float(customer.card_balance) - float(subscription.final_price)
        subscription.is_paid = True
        subscription.save(update_fields=['is_paid'])
        customer.save(update_fields=['card_balance'])

        return Response({'message': 'You have successfully purchased a subscription'}, status=status.HTTP_200_OK)

