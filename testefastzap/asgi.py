"""
ASGI config for testefastzap project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from fastzap.middlewares import JwtAuthMiddlewareStack
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import fastzap.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testefastzap.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JwtAuthMiddlewareStack(URLRouter(fastzap.routing.websocket_urlpatters))
})
