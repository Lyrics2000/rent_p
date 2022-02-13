
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = get_asgi_application()

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from homepage.websockets.routing import ws_urlpattern

application = ProtocolTypeRouter({
    'http':app,
    'websocket':AuthMiddlewareStack(URLRouter(ws_urlpattern))
}) 
