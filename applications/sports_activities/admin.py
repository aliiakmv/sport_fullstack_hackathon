from django.contrib import admin

from applications.sports_activities.models import SportsActivity, Trainer

admin.site.register(SportsActivity)
admin.site.register(Trainer)
