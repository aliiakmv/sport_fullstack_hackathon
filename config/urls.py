from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title='Fullstack hackathon',
        default_version='v1',
        description='Sport'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger')),

    path('api/v1/account/', include('applications.account.urls')),
    path('api/v1/sport_sections/', include('applications.section.urls')),
    path('api/v1/feedback/', include('applications.feedback.urls')),
    # path('api/v1/subscriptions/', include('applications.payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
