from django.contrib import admin

from applications.section.models import Section, Category

admin.site.register(Category)
admin.site.register(Section)
