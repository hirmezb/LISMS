"""
Database models for the Laboratory Information Management System.

These models reflect the tables defined in the provided Microsoft SQL
Server schema.  Relationships between entities are expressed through
Django's `ForeignKey` and `OneToOneField` constructs.  Many of the
identifiers use auto‑incrementing ``BigAutoField`` primary keys for
simplicity.  If you need to preserve the original decimal primary keys
(e.g. for integration with an existing database), adjust the field
definitions accordingly.
"""

from __future__ import annotations

from django.db import models


class UserAccount(models.Model):
    """Represents a user within the laboratory system."""

    account_username = models.CharField(max_length=64, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField(max_length=255)
    department = models.CharField(max_length=255)
    training_completed = models.BooleanField()
    is_analyst = models.BooleanField()
    is_administrator = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.account_username} ({self.first_name} {self.last_name})"


class Analyst(models.Model):
    """Additional information for users who are analysts."""

    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="analyst")
    access_level = models.PositiveSmallIntegerField()
    analyst_supervisor = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Analyst {self.user_account.account_username}"


class Administrator(models.Model):
    """Additional information for users who are administrators."""

    user_account = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="administrator")
    is_supervisor = models.BooleanField()

    def __str__(self) -> str:
        return f"Administrator {self.user_account.account_username}"


class SOP(models.Model):
    """Standard Operating Procedure metadata."""

    sop_name = models.CharField(max_length=16, unique=True)
    version_number = models.DecimalField(max_digits=3, decimal_places=1)
    effective_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.sop_name} v{self.version_number}"


class UserSOPAction(models.Model):
    """Tracks quality assurance workflow actions on SOPs."""

    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    qa_author = models.CharField(max_length=64)
    qa_reviewer = models.CharField(max_length=64)
    qa_approver = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"SOP action by {self.user_account.account_username} on {self.sop.sop_name}"


class Client(models.Model):
    """Represents an external customer or business partner."""

    client_name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.client_name


class Warehouse(models.Model):
    """Warehouse facilities at which samples or reagents are stored."""

    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    warehouse_technician = models.CharField(max_length=64)
    warehouse_facility = models.CharField(max_length=64)
    warehouse_company = models.CharField(max_length=64)

    class Meta:
        unique_together = ("warehouse_facility", "warehouse_company")

    def __str__(self) -> str:
        return f"{self.warehouse_company} – {self.warehouse_facility}"


class WarehouseClientLink(models.Model):
    """Links warehouses to clients for shipment records."""

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    quantity_shipped = models.DecimalField(max_digits=6, decimal_places=0)
    delivery_service = models.CharField(max_length=64)
    shipping_time = models.DateTimeField()
    delivery_time = models.DateTimeField()
    acceptable_delivery = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.warehouse} → {self.client} ({self.delivery_service})"


class Location(models.Model):
    """Physical locations in which samples or equipment reside."""

    location_type = models.CharField(max_length=64)
    room_number = models.IntegerField()

    class Meta:
        unique_together = ("location_type", "room_number")

    def __str__(self) -> str:
        return f"{self.location_type} {self.room_number}"


class Equipment(models.Model):
    """Equipment used for testing and sample manipulation."""

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=64)
    min_use_range = models.DecimalField(max_digits=16, decimal_places=6)
    max_use_range = models.DecimalField(max_digits=16, decimal_places=6)
    in_use = models.BooleanField()

    def __str__(self) -> str:
        return self.equipment_name


class MaintenanceLog(models.Model):
    """Maintenance records for equipment."""

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    service_date = models.DateField()
    service_description = models.TextField()
    service_interval = models.CharField(max_length=64)
    next_service_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.equipment.equipment_name} serviced on {self.service_date}"


class Sample(models.Model):
    """Samples tracked by the system."""

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64)
    product_stage = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=6, decimal_places=0)
    time_received = models.DateTimeField()
    sample_type = models.CharField(max_length=1, choices=(
        ("I", "In Process"),
        ("S", "Stability"),
        ("F", "Finished Product"),
    ))
    storage_conditions = models.CharField(max_length=5)

    def __str__(self) -> str:
        return f"Sample {self.id}: {self.product_name}"


class InProcess(models.Model):
    """Additional attributes for in‑process samples."""

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    time_sampled = models.DateTimeField()

    def __str__(self) -> str:
        return f"InProcess sample {self.sample_id}"


class Stability(models.Model):
    """Additional attributes for stability samples."""

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    stability_conditions = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Stability sample {self.sample_id}"


class FinishedProduct(models.Model):
    """Additional attributes for finished product samples."""

    sample = models.OneToOneField(Sample, on_delete=models.CASCADE, primary_key=True)
    product_lot_number = models.BigIntegerField()

    def __str__(self) -> str:
        return f"FinishedProduct sample {self.sample_id}"


class UserSampleAction(models.Model):
    """Tracks which analysts handled which samples."""

    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    receiving_analyst = models.CharField(max_length=64)
    aliquoting_analyst = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self) -> str:
        return f"Action on sample {self.sample_id} by {self.user_account.account_username}"


class Test(models.Model):
    """Laboratory tests performed on samples."""

    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    min_acceptable_result = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    max_acceptable_result = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)

    def __str__(self) -> str:
        return f"Test {self.id} ({self.sop.sop_name})"


class SampleTestLink(models.Model):
    """Associates samples with tests and their results."""

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    testing_analyst = models.CharField(max_length=64)
    reviewing_analyst = models.CharField(max_length=64)
    test_result = models.DecimalField(max_digits=16, decimal_places=6)
    deadline = models.DateTimeField()
    pass_or_fail = models.BooleanField()

    def __str__(self) -> str:
        return f"Result for sample {self.sample_id} / test {self.test_id}"


class TestEquipmentLink(models.Model):
    """Associates tests with the equipment they utilize."""

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Equipment {self.equipment_id} on test {self.test_id}"


class Reagent(models.Model):
    """Chemical reagents used within tests."""

    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    reagent_name = models.CharField(max_length=255)
    cas_number = models.CharField(max_length=12)
    lot_number = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    manufacturing_date = models.DateField()
    expiration_date = models.DateField()

    def __str__(self) -> str:
        return self.reagent_name


class UserReagentAction(models.Model):
    """Tracks actions on reagents by users."""

    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    reagent_manager = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Reagent action by {self.user_account.account_username} on {self.reagent.reagent_name}"


class TestReagentLink(models.Model):
    """Associates reagents with tests and the volume used."""

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    reagent = models.ForeignKey(Reagent, on_delete=models.CASCADE)
    volume_used = models.DecimalField(max_digits=16, decimal_places=6)

    def __str__(self) -> str:
        return f"{self.volume_used} of {self.reagent.reagent_name} in test {self.test_id}"


class VersionChange(models.Model):
    """Captures the history of SOP version updates."""

    old_version_number = models.DecimalField(max_digits=3, decimal_places=1)
    new_version_number = models.DecimalField(max_digits=3, decimal_places=1)
    old_effective_date = models.DateField()
    new_effective_date = models.DateField()
    sop = models.ForeignKey(SOP, on_delete=models.CASCADE)
    change_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.sop.sop_name} changed {self.old_version_number}→{self.new_version_number}"