"""ASGI config for the myntra_clone project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myntra.settings")

application = get_asgi_application()
