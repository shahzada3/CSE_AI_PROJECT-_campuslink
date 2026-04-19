import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_collab.settings')

django_asgi_app = get_asgi_application()

# SAFE fallback (prevents crash)
try:
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import chat.routing

    application = ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
        ),
    })

except Exception as e:
    print("WebSocket disabled due to error:", e)
    application = django_asgi_app