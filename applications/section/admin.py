from django.contrib import admin

from applications.section.models import Section, Category, ParsingGym

admin.site.register(Category)
admin.site.register(Section)
admin.site.register(ParsingGym)