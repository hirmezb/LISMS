"""
API views for the LISMS back end.

Each model is exposed as a RESTful resource through a DRF ``ModelViewSet``.
Additional endpoints provide aggregated data for dashboards, such as the
number of clients per warehouse and the average time between SOP
effective dates.
"""

from __future__ import annotations

from django.db.models import Avg, Count, F, Func, Value
from django.db.models.functions import Cast
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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
from .serializers import (
    AdministratorSerializer,
    AnalystSerializer,
    ClientSerializer,
    EquipmentSerializer,
    FinishedProductSerializer,
    InProcessSerializer,
    LocationSerializer,
    MaintenanceLogSerializer,
    ReagentSerializer,
    SampleSerializer,
    SampleTestLinkSerializer,
    SOPSerializer,
    StabilitySerializer,
    TestSerializer,
    TestEquipmentLinkSerializer,
    TestReagentLinkSerializer,
    UserAccountSerializer,
    UserReagentActionSerializer,
    UserSampleActionSerializer,
    UserSOPActionSerializer,
    VersionChangeSerializer,
    WarehouseClientLinkSerializer,
    WarehouseSerializer,
    DashboardWarehouseClientsSerializer,
    DashboardVersionChangeSerializer,
)


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by("id")
    serializer_class = UserAccountSerializer


class AnalystViewSet(viewsets.ModelViewSet):
    queryset = Analyst.objects.select_related("user_account").all()
    serializer_class = AnalystSerializer


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.select_related("user_account").all()
    serializer_class = AdministratorSerializer


class SOPViewSet(viewsets.ModelViewSet):
    queryset = SOP.objects.all()
    serializer_class = SOPSerializer


class UserSOPActionViewSet(viewsets.ModelViewSet):
    queryset = UserSOPAction.objects.select_related("user_account", "sop").all()
    serializer_class = UserSOPActionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.select_related("sop").all()
    serializer_class = WarehouseSerializer


class WarehouseClientLinkViewSet(viewsets.ModelViewSet):
    queryset = WarehouseClientLink.objects.select_related("warehouse", "client").all()
    serializer_class = WarehouseClientLinkSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.select_related("location", "sop").all()
    serializer_class = EquipmentSerializer


class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.select_related("equipment", "sop").all()
    serializer_class = MaintenanceLogSerializer


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.select_related("location", "warehouse", "sop").all()
    serializer_class = SampleSerializer


class InProcessViewSet(viewsets.ModelViewSet):
    queryset = InProcess.objects.select_related("sample").all()
    serializer_class = InProcessSerializer


class StabilityViewSet(viewsets.ModelViewSet):
    queryset = Stability.objects.select_related("sample").all()
    serializer_class = StabilitySerializer


class FinishedProductViewSet(viewsets.ModelViewSet):
    queryset = FinishedProduct.objects.select_related("sample").all()
    serializer_class = FinishedProductSerializer


class UserSampleActionViewSet(viewsets.ModelViewSet):
    queryset = UserSampleAction.objects.select_related("user_account", "sample").all()
    serializer_class = UserSampleActionSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.select_related("user_account", "sop").all()
    serializer_class = TestSerializer


class SampleTestLinkViewSet(viewsets.ModelViewSet):
    queryset = SampleTestLink.objects.select_related("sample", "test").all()
    serializer_class = SampleTestLinkSerializer


class TestEquipmentLinkViewSet(viewsets.ModelViewSet):
    queryset = TestEquipmentLink.objects.select_related("test", "equipment").all()
    serializer_class = TestEquipmentLinkSerializer


class ReagentViewSet(viewsets.ModelViewSet):
    queryset = Reagent.objects.select_related("sop").all()
    serializer_class = ReagentSerializer


class UserReagentActionViewSet(viewsets.ModelViewSet):
    queryset = UserReagentAction.objects.select_related("user_account", "reagent").all()
    serializer_class = UserReagentActionSerializer


class TestReagentLinkViewSet(viewsets.ModelViewSet):
    queryset = TestReagentLink.objects.select_related("test", "reagent").all()
    serializer_class = TestReagentLinkSerializer


class VersionChangeViewSet(viewsets.ModelViewSet):
    queryset = VersionChange.objects.select_related("sop").all()
    serializer_class = VersionChangeSerializer


class DashboardWarehouseClientsView(APIView):
    """Returns the number of distinct clients served by each warehouse facility."""

    def get(self, request, format=None):  # type: ignore[override]
        data = (
            WarehouseClientLink.objects
            .values("warehouse__warehouse_facility")
            .annotate(total_clients=Count("client", distinct=True))
            .order_by("-total_clients")
        )
        serializer = DashboardWarehouseClientsSerializer(data, many=True)
        return Response(serializer.data)


class DashboardVersionChangeView(APIView):
    """Returns the average number of days between SOP effective date changes."""

    def get(self, request, format=None):  # type: ignore[override]
        # Compute the difference in days between the old and new effective dates
        data = (
            VersionChange.objects
            .annotate(days_between=Cast(F("new_effective_date"), models.DateField()) - Cast(F("old_effective_date"), models.DateField()))
            .values("sop__sop_name")
            .annotate(average_days_between_effective_dates=Avg(F("days_between")))
            .order_by("sop__sop_name")
        )
        # Convert timedeltas to days (if aggregated as timedeltas).  The ORM will return
        # ``datetime.timedelta`` objects for the average; extract the ``days`` attribute.
        formatted = []
        for item in data:
            avg_period = item["average_days_between_effective_dates"]
            days = avg_period.days if hasattr(avg_period, "days") else avg_period
            formatted.append({
                "sop_name": item["sop__sop_name"],
                "average_days_between_effective_dates": days,
            })
        serializer = DashboardVersionChangeSerializer(formatted, many=True)
        return Response(serializer.data)