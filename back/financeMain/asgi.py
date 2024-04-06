from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat.routing
from chat.middlewares import TokenAuthMiddleWare

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleWare(
            AllowedHostsOriginValidator(
                URLRouter(
                    chat.routing.websocket_urlpatterns
                )
            )
        )
    }
)
