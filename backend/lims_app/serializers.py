"""
Serializers translate Django model instances into JSON and back again.

The LISMS API uses Django REST Framework (DRF) for serialization.  Each
model has an associated ``ModelSerializer`` that exposes all fields by
default.  Additional serializers aggregate information for dashboard
visualisations.
"""

from __future__ import annotations

from rest_framework import serializers

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


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"


class AnalystSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)

    class Meta:
        model = Analyst
        fields = "__all__"


class AdministratorSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)

    class Meta:
        model = Administrator
        fields = "__all__"


class SOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOP
        fields = "__all__"


class UserSOPActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSOPAction
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class WarehouseClientLinkSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = WarehouseClientLink
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = "__all__"


class MaintenanceLogSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(read_only=True)
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = MaintenanceLog
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = Sample
        fields = "__all__"


class InProcessSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)

    class Meta:
        model = InProcess
        fields = "__all__"


class StabilitySerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)

    class Meta:
        model = Stability
        fields = "__all__"


class FinishedProductSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)

    class Meta:
        model = FinishedProduct
        fields = "__all__"


class UserSampleActionSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)
    sample = SampleSerializer(read_only=True)

    class Meta:
        model = UserSampleAction
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = Test
        fields = "__all__"


class SampleTestLinkSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(read_only=True)
    test = TestSerializer(read_only=True)

    class Meta:
        model = SampleTestLink
        fields = "__all__"


class TestEquipmentLinkSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = TestEquipmentLink
        fields = "__all__"


class ReagentSerializer(serializers.ModelSerializer):
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = Reagent
        fields = "__all__"


class UserReagentActionSerializer(serializers.ModelSerializer):
    user_account = UserAccountSerializer(read_only=True)
    reagent = ReagentSerializer(read_only=True)

    class Meta:
        model = UserReagentAction
        fields = "__all__"


class TestReagentLinkSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    reagent = ReagentSerializer(read_only=True)

    class Meta:
        model = TestReagentLink
        fields = "__all__"


class VersionChangeSerializer(serializers.ModelSerializer):
    sop = SOPSerializer(read_only=True)

    class Meta:
        model = VersionChange
        fields = "__all__"


class DashboardWarehouseClientsSerializer(serializers.Serializer):
    """Aggregates the number of clients per warehouse."""

    warehouse_facility = serializers.CharField()
    total_clients = serializers.IntegerField()


class DashboardVersionChangeSerializer(serializers.Serializer):
    """Aggregates average days between SOP effective dates."""

    sop_name = serializers.CharField()
    average_days_between_effective_dates = serializers.FloatField()