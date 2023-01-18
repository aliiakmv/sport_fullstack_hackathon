from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import View
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.payments.models import Customer, Subscription
from applications.payments.permissions import IsSubscriptionOwner
from applications.payments.serializers import SubscriptionSerializer


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriptionOwner]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

