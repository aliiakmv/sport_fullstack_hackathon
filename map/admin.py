from django.contrib import admin
from .models import Section, Category, ParsingGym

# Register your models here.

admin.site.register(Section)
admin.site.register(Category)

admin.site.register(ParsingGym)