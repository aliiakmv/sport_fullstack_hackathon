from django.contrib import admin

from applications.feedback.models import Favorite, Rating, Like, Review

admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(Review)
