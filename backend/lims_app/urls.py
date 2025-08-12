"""
Routes for the LISMS API.

This module wires up model view sets into a single router under the
``/api/`` prefix defined in ``lims_project/urls.py``.  Additional
non‑standard endpoints for dashboard data are registered separately.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


# Create a router and register our viewsets.  The router automatically
# determines the URL conf for common operations (list, create, retrieve,
# update, destroy) on each model.
router = DefaultRouter()
router.register(r"users", views.UserAccountViewSet)
router.register(r"analysts", views.AnalystViewSet)
router.register(r"administrators", views.AdministratorViewSet)
router.register(r"sops", views.SOPViewSet)
router.register(r"sop-actions", views.UserSOPActionViewSet)
router.register(r"clients", views.ClientViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"warehouse-client-links", views.WarehouseClientLinkViewSet)
router.register(r"locations", views.LocationViewSet)
router.register(r"equipment", views.EquipmentViewSet)
router.register(r"maintenance-logs", views.MaintenanceLogViewSet)
router.register(r"samples", views.SampleViewSet)
router.register(r"in-process", views.InProcessViewSet)
router.register(r"stability", views.StabilityViewSet)
router.register(r"finished-products", views.FinishedProductViewSet)
router.register(r"user-sample-actions", views.UserSampleActionViewSet)
router.register(r"tests", views.TestViewSet)
router.register(r"sample-test-links", views.SampleTestLinkViewSet)
router.register(r"test-equipment-links", views.TestEquipmentLinkViewSet)
router.register(r"reagents", views.ReagentViewSet)
router.register(r"user-reagent-actions", views.UserReagentActionViewSet)
router.register(r"test-reagent-links", views.TestReagentLinkViewSet)
router.register(r"version-changes", views.VersionChangeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # Custom dashboard endpoints
    path("dashboard/warehouse-clients/", views.DashboardWarehouseClientsView.as_view(), name="dashboard-warehouse-clients"),
    path("dashboard/version-changes/", views.DashboardVersionChangeView.as_view(), name="dashboard-version-changes"),
]