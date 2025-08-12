"""
Django admin registration for LISMS models.

Registering models with the admin site allows administrators to inspect
and edit data through Django's built‑in admin interface.
"""

from django.contrib import admin

from .models import (
    Administrator,
    Analyst,
    Client,
    Equipment,
    FinishedProduct,
    InProcess,
    Location,
    MaintenanceLog,
    Reagent,
    Sample,
    SampleTestLink,
    SOP,
    Stability,
    Test,
    TestEquipmentLink,
    TestReagentLink,
    UserAccount,
    UserReagentAction,
    UserSampleAction,
    UserSOPAction,
    VersionChange,
    Warehouse,
    WarehouseClientLink,
)


models_to_register = [
    UserAccount,
    Analyst,
    Administrator,
    SOP,
    UserSOPAction,
    Client,
    Warehouse,
    WarehouseClientLink,
    Location,
    Equipment,
    MaintenanceLog,
    Sample,
    InProcess,
    Stability,
    FinishedProduct,
    UserSampleAction,
    Test,
    SampleTestLink,
    TestEquipmentLink,
    Reagent,
    UserReagentAction,
    TestReagentLink,
    VersionChange,
]

for model in models_to_register:
    admin.site.register(model)