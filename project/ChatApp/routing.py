from django.urls import re_path

from .consumers import ChatConsumer,P2P

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
    # re_path(r'ws/p2pchat/(?P<room_name>\w+)/$', P2P),
    re_path(r'ws/p2pchat/(?P<room_name>\w+)/$', P2P),
]