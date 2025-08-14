import os
from django.core.asgi import get_asgi_application

# Get environment and configure settings module
environment = os.getenv('ENVIRONMENT', 'local')
settings_module = f'config.settings.{environment}'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# Basic ASGI application (HTTP only)
application = get_asgi_application()

# Optional: WebSocket support (uncomment if needed)
# from channels.routing import ProtocolTypeRouter, URLRouter
# from core import routing
# 
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter(routing.websocket_urlpatterns),
# })
