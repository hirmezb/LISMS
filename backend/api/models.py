from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    user_account_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_account')
    account_username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    training_completed = models.BooleanField()
    is_analyst = models.CharField(max_length=1)
    is_administrator = models.CharField(max_length=1)

class Analyst(models.Model):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    access_level = models.DecimalField(max_digits=1, decimal_places=0)
    analyst_supervisor = models.CharField(max_length=64)

class Administrator(models.Model):
    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    is_supervisor = models.CharField(max_length=1)

class SOP(models.Model):
    sop_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    sop_name = models.CharField(max_length=16)
    version_number = models.DecimalField(max_digits=3, decimal_places=1)
    effective_date = models.DateField()

class UserSOPAction(models.Model):
    user_sop_action_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    qa_author = models.CharField(max_length=64)
    qa_reviewer = models.CharField(max_length=64)
    qa_approver = models.CharField(max_length=64)

class Client(models.Model):
    client_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    client_name = models.CharField(max_length=64)

class Warehouse(models.Model):
    warehouse_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    warehouse_technician = models.CharField(max_length=64)
    warehouse_facility = models.CharField(max_length=64)
    warehouse_company = models.CharField(max_length=64)

class WarehouseClientLink(models.Model):
    warehouse_client_link_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    quantity_shipped = models.DecimalField(max_digits=4, decimal_places=0)
    delivery_service = models.CharField(max_length=64)
    shipping_time = models.DateTimeField()
    delivery_time = models.DateTimeField()
    acceptable_delivery = models.BooleanField()

class Location(models.Model):
    location_id = models.DecimalField(max_digits=5, decimal_places=0, primary_key=True)
    location_type = models.CharField(max_length=64, null=True, blank=True)
    room_number = models.DecimalField(max_digits=5, decimal_places=0)

class Equipment(models.Model):
    equipment_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=64)
    min_use_range = models.DecimalField(max_digits=10, decimal_places=6)
    max_use_range = models.DecimalField(max_digits=10, decimal_places=6)
    in_use = models.BooleanField()

class MaintenanceLog(models.Model):
    maintenance_log_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    service_date = models.DateField()
    service_description = models.CharField(max_length=4000)
    service_interval = models.CharField(max_length=64)
    next_service_date = models.DateField()

class Sample(models.Model):
    sample_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64)
    product_stage = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=4, decimal_places=0)
    time_received = models.DateTimeField()
    sample_type = models.CharField(max_length=1)
    storage_conditions = models.CharField(max_length=5)

class InProcess(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    time_sampled = models.DateTimeField()

class Stability(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    stability_conditions = models.CharField(max_length=64)

class FinishedProduct(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    product_lot_number = models.DecimalField(max_digits=16, decimal_places=0)

class UserSampleAction(models.Model):
    user_sample_action_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    receiving_analyst = models.CharField(max_length=64)
    aliquoting_analyst = models.CharField(max_length=64, null=True, blank=True)

class Test(models.Model):
    test_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    min_acceptable_result = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    max_acceptable_result = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

class SampleTestLink(models.Model):
    sample_test_link_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    testing_analyst = models.CharField(max_length=64)
    reviewing_analyst = models.CharField(max_length=64)
    test_result = models.DecimalField(max_digits=10, decimal_places=6)
    deadline = models.DateTimeField()
    pass_or_fail = models.BooleanField()

class TestEquipmentLink(models.Model):
    test_equipment_link_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

class Reagent(models.Model):
    reagent_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    reagent_name = models.CharField(max_length=255)
    cas_number = models.CharField(max_length=12)
    lot_number = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    manufacturing_date = models.DateField()
    expiration_date = models.DateField()

class UserReagentAction(models.Model):
    user_reagent_action_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    reagent_manager = models.CharField(max_length=64)

class TestReagentLink(models.Model):
    test_reagent_link_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    volume_used = models.DecimalField(max_digits=10, decimal_places=6)

class VersionChange(models.Model):
    version_change_id = models.DecimalField(max_digits=12, decimal_places=0, primary_key=True)
    old_version_number = models.DecimalField(max_digits=3, decimal_places=1)
    new_version_number = models.DecimalField(max_digits=3, decimal_places=1)
    old_effective_date = models.DateField()
    new_effective_date = models.DateField()
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    change_date = models.DateField()
