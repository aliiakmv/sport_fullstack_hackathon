from rest_framework import serializers

from applications.payments.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(required=False)

    class Meta:
        model = Subscription
        fields = '__all__'

