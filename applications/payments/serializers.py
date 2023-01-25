from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from applications.payments.models import Subscription, Customer
from applications.payments.tasks import send_subscription_key_email
from applications.payments.validators import CCNumberValidator


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(required=False)
    phone = PhoneNumberField(max_length=13, min_length=10)
    card_number = serializers.CharField(max_length=19, min_length=12, validators=[CCNumberValidator()])

    class Meta:
        model = Customer
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    customer = serializers.EmailField(required=False)
    final_price = serializers.IntegerField(required=False)

    class Meta:
        model = Subscription
        fields = '__all__'

    @staticmethod
    def validate_final_price(attrs):
        final_price = attrs['final_price']
        if final_price > Customer.card_balance:
            raise serializers.ValidationError('На вашей карте недостаточно средств')
        return attrs

    @staticmethod
    def create(validated_data):
        subscription = Subscription.objects.create( **validated_data)
        send_subscription_key_email.delay(email=subscription.customer.email, money=subscription.classes.price,
                                          subscription_key=subscription.subscription_key)
        return subscription
