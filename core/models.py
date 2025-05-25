from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        WORKER = "WORKER", _("Healthcare Worker")

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.WORKER)
    country = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    facility = models.CharField(max_length=200, blank=True)


class SideEffectReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suspected_drug = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    side_effects = models.TextField()
    severity = models.CharField(max_length=10, choices=[
        ("Mild", "Mild"),
        ("Moderate", "Moderate"), 
        ("Severe", "Severe")
    ])
    aware_of_allergy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Side effect report for {self.suspected_drug} by {self.user.username}"

class DrugResistanceReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    retreated_within_30_days = models.BooleanField()
    same_disease = models.CharField(max_length=200)
    first_diagnosis_method = models.CharField(max_length=200)
    second_diagnosis_method = models.CharField(max_length=200)
    treatment_details = models.TextField()
    brand_name = models.CharField(max_length=200, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Drug(models.Model):
    name = models.CharField(max_length=200)

class Disease(models.Model):
    name = models.CharField(max_length=200)

class Facility(models.Model):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
