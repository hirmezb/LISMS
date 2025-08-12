"""
URL configuration for the LISMS back end.

The ``urlpatterns`` list routes incoming HTTP requests to the appropriate view.
All REST API endpoints are namespaced under ``/api/`` and defined in
``lims_app/urls.py``.  The built‑in Django admin is available under
``/admin/`` for data inspection and management.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("lims_app.urls")),
]