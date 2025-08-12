"""
ASGI config for lims_project.

This module exposes the ASGI application used by Django's asynchronous
support.  It is the entry point for ASGI‑compatible web servers.  See
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/ for more
information.
"""

import os

from django.core.asgi import get_asgi_application  # type: ignore


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lims_project.settings")

application = get_asgi_application()