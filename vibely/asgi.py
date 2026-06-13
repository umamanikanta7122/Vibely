import os

from django.core.asgi import (
    get_asgi_application
)

# SETTINGS FIRST
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'vibely.settings'
)

# DJANGO INIT FIRST
django_asgi_app = get_asgi_application()
from posts.routing import (
    websocket_urlpatterns
)

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter
)

from channels.auth import (
    AuthMiddlewareStack
)

# IMPORT AFTER DJANGO IS READY



application = ProtocolTypeRouter({

    "http":
    django_asgi_app,

    "websocket":
    AuthMiddlewareStack(

        URLRouter(
            websocket_urlpatterns
        )

    ),

})