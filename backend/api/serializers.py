from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    UserAccount, Analyst, Administrator, SOP, UserSOPAction, Client, Warehouse,
    WarehouseClientLink, Location, Equipment, MaintenanceLog, Sample, InProcess,
    Stability, FinishedProduct, UserSampleAction, Test, SampleTestLink,
    TestEquipmentLink, Reagent, UserReagentAction, TestReagentLink, VersionChange
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserAccount
        fields = '__all__'
        extra_kwargs = {
            'user_account_id': {'read_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_account = UserAccount.objects.create(user=user, **validated_data)

        if validated_data.get('is_analyst') == 'Y':
            Analyst.objects.create(user_account=user_account, access_level=1, analyst_supervisor='Default Supervisor')
        elif validated_data.get('is_administrator') == 'Y':
            Administrator.objects.create(user_account=user_account, is_supervisor='N')

        return user_account

class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyst
        fields = '__all__'
        extra_kwargs = {
            'user_account': {'read_only': True}
        }

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'
        extra_kwargs = {
            'user_account': {'read_only': True}
        }

class SOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOP
        fields = '__all__'
        extra_kwargs = {
            'sop_id': {'read_only': True}
        }

class UserSOPActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSOPAction
        fields = '__all__'
        extra_kwargs = {
            'user_sop_action_id': {'read_only': True}
        }

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'client_id': {'read_only': True}
        }

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        extra_kwargs = {
            'warehouse_id': {'read_only': True}
        }

class WarehouseClientLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseClientLink
        fields = '__all__'
        extra_kwargs = {
            'warehouse_client_link_id': {'read_only': True}
        }

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        extra_kwargs = {
            'location_id': {'read_only': True}
        }

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'
        extra_kwargs = {
            'equipment_id': {'read_only': True}
        }

class MaintenanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLog
        fields = '__all__'
        extra_kwargs = {
            'maintenance_log_id': {'read_only': True}
        }

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'
        extra_kwargs = {
            'sample_id': {'read_only': True}
        }

class InProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = InProcess
        fields = '__all__'
        extra_kwargs = {
            'sample': {'read_only': True}
        }

class StabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stability
        fields = '__all__'
        extra_kwargs = {
            'sample': {'read_only': True}
        }

class FinishedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishedProduct
        fields = '__all__'
        extra_kwargs = {
            'sample': {'read_only': True}
        }

class UserSampleActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSampleAction
        fields = '__all__'
        extra_kwargs = {
            'user_sample_action_id': {'read_only': True}
        }

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {
            'test_id': {'read_only': True}
        }

class SampleTestLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleTestLink
        fields = '__all__'
        extra_kwargs = {
            'sample_test_link_id': {'read_only': True}
        }

class TestEquipmentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestEquipmentLink
        fields = '__all__'
        extra_kwargs = {
            'test_equipment_link_id': {'read_only': True}
        }

class ReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reagent
        fields = '__all__'
        extra_kwargs = {
            'reagent_id': {'read_only': True}
        }

class UserReagentActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReagentAction
        fields = '__all__'
        extra_kwargs = {
            'user_reagent_action_id': {'read_only': True}
        }

class TestReagentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestReagentLink
        fields = '__all__'
        extra_kwargs = {
            'test_reagent_link_id': {'read_only': True}
        }

class VersionChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionChange
        fields = '__all__'
        extra_kwargs = {
            'version_change_id': {'read_only': True}
        }
