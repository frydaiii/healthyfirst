from django.contrib.auth import models as auth_models
from django.db import models as base_models


class Person(auth_models.AbstractUser):
    MANAGER = 'MN'
    STAFF = 'ST'
    ROLE = [
        (MANAGER, 'Manager'),
        (STAFF, 'Staff'),
    ]

    role = base_models.CharField(max_length=2, choices=ROLE, default=STAFF)
    id_area = base_models.IntegerField()

    def is_manager(self):
        if self.role == self.MANAGER:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean(exclude=['password'])
        return super().save(*args, **kwargs)


class Premise(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    name = base_models.CharField(max_length=255)
    address = base_models.CharField(max_length=255)
    sub_district = base_models.CharField(max_length=255)
    district = base_models.CharField(max_length=255)
    phone_number = base_models.IntegerField()
    id_business_type = base_models.IntegerField()
    id_certificate = base_models.IntegerField()


class Certificate(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    id_business_type = base_models.IntegerField()
    issued_date = base_models.DateField(auto_now=True)
    expired_date = base_models.DateField()
    serie = base_models.CharField(max_length=10)


class BusinessType(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    name = base_models.CharField(max_length=50)
    description = base_models.CharField(max_length=255)


class InspectionPlan(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    inspection_date = base_models.DateField()
    sample_needed = base_models.BooleanField(default=False)
    violate = base_models.BooleanField(default=False)
    id_premise = base_models.IntegerField()
    id_sample = base_models.IntegerField()


class Sample(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    id_premise = base_models.IntegerField()
    accreditation_premise = base_models.CharField(max_length=255)
    accreditation_status = base_models.CharField(max_length=255)
    result_date = base_models.DateField()
    result_valid = base_models.BooleanField()


class Area(base_models.Model):
    id = base_models.IntegerField(primary_key=True)
    name = base_models.CharField(max_length=255)
    type = base_models.CharField(max_length=255)
