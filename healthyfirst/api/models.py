from django.contrib.auth import models as auth_models
from django.db import models as base_models


class Person(auth_models.AbstractUser):

    is_manager = base_models.BooleanField(default=False)
    id_area = base_models.IntegerField()

    def save(self, *args, **kwargs):
        self.full_clean(exclude=['password'])
        return super().save(*args, **kwargs)


class Premise(base_models.Model):
    name = base_models.CharField(max_length=255)
    address = base_models.CharField(max_length=255)
    phone_number = base_models.IntegerField()
    id_area = base_models.IntegerField(default=0)
    id_business_type = base_models.IntegerField()
    id_certificate = base_models.IntegerField(blank=True, null=True)


class Certificate(base_models.Model):
    id_business_type = base_models.IntegerField()
    issued_date = base_models.DateField(auto_now=True)
    expired_date = base_models.DateField()
    series = base_models.CharField(max_length=10)
    status = base_models.CharField(null=True, blank=True, max_length=255)
    file_path = base_models.CharField(null=True, blank=True, max_length=255)


class BusinessType(base_models.Model):
    name = base_models.CharField(max_length=50)
    description = base_models.CharField(max_length=255)


class InspectionPlan(base_models.Model):
    inspection_date = base_models.DateField()
    sample_needed = base_models.BooleanField(default=False)
    violate = base_models.BooleanField(default=False)
    status = base_models.CharField(null=True, blank=True, max_length=255)
    id_premise = base_models.IntegerField()
    id_sample = base_models.IntegerField(null=True)


class Sample(base_models.Model):
    id_premise = base_models.IntegerField()
    accreditation_premise = base_models.CharField(max_length=255)
    accreditation_status = base_models.CharField(max_length=255)
    result_date = base_models.DateField()
    result_valid = base_models.BooleanField()


class Area(base_models.Model):
    name = base_models.CharField(max_length=255)
    type = base_models.CharField(max_length=255)
