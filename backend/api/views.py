from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import (
    UserAccount, Analyst, Administrator, SOP, UserSOPAction, Client, Warehouse,
    WarehouseClientLink, Location, Equipment, MaintenanceLog, Sample, InProcess,
    Stability, FinishedProduct, UserSampleAction, Test, SampleTestLink,
    TestEquipmentLink, Reagent, UserReagentAction, TestReagentLink, VersionChange
)
from .serializers import (
    UserSerializer, UserAccountSerializer, AnalystSerializer, AdministratorSerializer, SOPSerializer,
    UserSOPActionSerializer, ClientSerializer, WarehouseSerializer,
    WarehouseClientLinkSerializer, LocationSerializer, EquipmentSerializer,
    MaintenanceLogSerializer, SampleSerializer, InProcessSerializer,
    StabilitySerializer, FinishedProductSerializer, UserSampleActionSerializer,
    TestSerializer, SampleTestLinkSerializer, TestEquipmentLinkSerializer,
    ReagentSerializer, UserReagentActionSerializer, TestReagentLinkSerializer,
    VersionChangeSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    # Ensures user being created does not already exist
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Specified who can use this view to create new User.
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return UserAccount.objects.filter(user__id=user_id)
        return super().get_queryset()

class AnalystViewSet(viewsets.ModelViewSet):
    queryset = Analyst.objects.all()
    serializer_class = AnalystSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_account_id = self.request.query_params.get('user_account_id')
        if user_account_id:
            return Analyst.objects.filter(user_account_id=user_account_id)
        return super().get_queryset()

class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_account_id = self.request.query_params.get('user_account_id')
        if user_account_id:
            return Administrator.objects.filter(user_account_id=user_account_id)
        return super().get_queryset()

class SOPViewSet(viewsets.ModelViewSet):
    queryset = SOP.objects.all()
    serializer_class = SOPSerializer
    permission_classes = [IsAuthenticated]

class UserSOPActionViewSet(viewsets.ModelViewSet):
    queryset = UserSOPAction.objects.all()
    serializer_class = UserSOPActionSerializer
    permission_classes = [IsAuthenticated]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

class WarehouseClientLinkViewSet(viewsets.ModelViewSet):
    queryset = WarehouseClientLink.objects.all()
    serializer_class = WarehouseClientLinkSerializer
    permission_classes = [IsAuthenticated]

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    permission_classes = [IsAuthenticated]

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        warehouse_id = self.request.query_params.get('warehouse_id')
        if warehouse_id:
            return Sample.objects.filter(warehouse_id=warehouse_id)
        return super().get_queryset()

class InProcessViewSet(viewsets.ModelViewSet):
    queryset = InProcess.objects.all()
    serializer_class = InProcessSerializer
    permission_classes = [IsAuthenticated]

class StabilityViewSet(viewsets.ModelViewSet):
    queryset = Stability.objects.all()
    serializer_class = StabilitySerializer
    permission_classes = [IsAuthenticated]

class FinishedProductViewSet(viewsets.ModelViewSet):
    queryset = FinishedProduct.objects.all()
    serializer_class = FinishedProductSerializer
    permission_classes = [IsAuthenticated]

class UserSampleActionViewSet(viewsets.ModelViewSet):
    queryset = UserSampleAction.objects.all()
    serializer_class = UserSampleActionSerializer
    permission_classes = [IsAuthenticated]

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        analyst_id = self.request.query_params.get('analyst_id')
        if analyst_id:
            return Test.objects.filter(user_account_id=analyst_id)
        return super().get_queryset()

class SampleTestLinkViewSet(viewsets.ModelViewSet):
    queryset = SampleTestLink.objects.all()
    serializer_class = SampleTestLinkSerializer
    permission_classes = [IsAuthenticated]

class TestEquipmentLinkViewSet(viewsets.ModelViewSet):
    queryset = TestEquipmentLink.objects.all()
    serializer_class = TestEquipmentLinkSerializer
    permission_classes = [IsAuthenticated]

class ReagentViewSet(viewsets.ModelViewSet):
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
    permission_classes = [IsAuthenticated]

class UserReagentActionViewSet(viewsets.ModelViewSet):
    queryset = UserReagentAction.objects.all()
    serializer_class = UserReagentActionSerializer
    permission_classes = [IsAuthenticated]

class TestReagentLinkViewSet(viewsets.ModelViewSet):
    queryset = TestReagentLink.objects.all()
    serializer_class = TestReagentLinkSerializer
    permission_classes = [IsAuthenticated]

class VersionChangeViewSet(viewsets.ModelViewSet):
    queryset = VersionChange.objects.all()
    serializer_class = VersionChangeSerializer
    permission_classes = [IsAuthenticated]

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
