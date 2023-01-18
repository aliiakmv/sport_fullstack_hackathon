from django.contrib import admin

from applications.payments.models import Customer, Subscription

admin.site.register(Customer)
admin.site.register(Subscription)