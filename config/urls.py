from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Team hackathon',
        default_version='v1',
        description='Courses'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
]