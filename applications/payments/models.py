import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from applications.payments.validators import CCNumberValidator
from applications.section.models import Section

User = get_user_model()


class Customer(models.Model):
    """Владелец абонемента"""
    CARD_TYPE_CHOICE = (
        ('visa', 'Visa'),
        ('elcart', 'Elcart'),
        ('mastercard', 'MasterCard'),
        ('unionpay', 'UnionPay'),
        ('american_express', 'American Express'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='month_subscriptions')
    phone = PhoneNumberField(max_length=13)
    card_type = models.CharField(CARD_TYPE_CHOICE, max_length=180)
    card_number = models.CharField(max_length=19, validators=[CCNumberValidator()])
    card_expiry_date = models.DateField(format(['%m/%y', '%m/%Y']))
    card_balance = models.DecimalField(max_digits=10, decimal_places=2)


class Subscription(models.Model):
    """Абонемент в зал/спортивную секцию"""
    CHOICE = (
        ('month', 'Month'),
        ('year', 'Year')
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    classes = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_key = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(CHOICE, max_length=50)
    discount = models.PositiveIntegerField(default=20)
    final_price = models.DecimalField(decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.final_price = float(self.classes.price) * (1 - (self.discount / 100))
        super().save(*args, **kwargs)
