"""WSGI config for the myntra_clone project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myntra.settings")

application = get_wsgi_application()
