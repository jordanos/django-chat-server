import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns
from common.channels_auth import CustomTokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

asgi_application = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": CustomTokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
