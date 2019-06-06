# # hanium/routing.py
# from channels.routing import ProtocolTypeRouter
#
# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
# })

# # hanium/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

#클라이언트와 채널 개발 서버와 연결이 맺어질 때 가장먼저 조사하여 어떤 타입의 연결인지 구분
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    #만약 WebSocket연결이라면 => AuthMiddlewareStack
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
