from django.db import models
from vaccine_centre.models import VaccineCentre

# Create your models here.

class Session(models.Model):
    centre =models.ForeignKey(VaccineCentre, null=True, on_delete = models.SET_NULL)
    session_id = models.CharField(max_length=6, null=True, unique=True)
    session_date = models.DateField(auto_now=False)
    avalable_capacity =models.CharField(max_length=10, null=True)
    slot = models.CharField(max_length=20, null=True)
