import os

import django
from channels.layers import get_channel_layer

from channels.routing import ProtocolTypeRouter, URLRouter

from .routing import websocket_urlpatterns

from channels.security.websocket import AllowedHostsOriginValidator

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({

    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns),
        )
    ),
})
