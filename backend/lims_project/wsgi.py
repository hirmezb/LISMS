"""
WSGI config for lims_project.

This exposes the WSGI callable as a module-level variable named
``application``.  Django's development server and WSGI servers (e.g.
Gunicorn, uWSGI) use this entry point to serve the application.
"""

import os

from django.core.wsgi import get_wsgi_application  # type: ignore


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lims_project.settings")

application = get_wsgi_application()