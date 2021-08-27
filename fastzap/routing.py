from django.urls import re_path

from .consumers import ChatConsumer

websocket_urlpatters = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', ChatConsumer.as_asgi()),
]