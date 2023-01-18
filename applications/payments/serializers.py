from rest_framework import serializers

from applications.payments.models import Subscription, Customer
from applications.payments.tasks import send_subscription_key_email
from applications.payments.validators import CCNumberValidator


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(required=False)
    card_number = serializers.CharField(max_length=19, min_length=12, default_validators = [CCNumberValidator()])

    class Meta:
        model = Customer
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(required=False)

    class Meta:
        model = Subscription
        fields = '__all__'

    @staticmethod
    def validate(attrs):
        customer = attrs['customer']
        final_price = attrs['final_price']
        if final_price > customer.card_balance:
            raise serializers.ValidationError('На вашей карте недостаточно средств')
        return attrs

    @staticmethod
    def create(self, validated_data):
        customer = validated_data['customer']
        payment = validated_data['final_price']
        subscription_key = validated_data['subscription_key']

        customer.card_balance -= payment
        customer.save(update_fields=['card_balance'])

        is_paid = validated_data['is_paid']
        is_paid = True

        subscription = Subscription.objects.create(**validated_data)
        send_subscription_key_email.delay(email=customer.user.email, money=payment, subscription_key=subscription_key)
        return subscription
