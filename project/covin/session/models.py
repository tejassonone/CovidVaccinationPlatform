from django.db import models
from vaccine_centre.models import VaccineCentre
from accounts.models import Beneficiary

# Create your models here.

class Session(models.Model):
    centre =models.ForeignKey(VaccineCentre, null=True, on_delete = models.SET_NULL)
    session_id = models.CharField(max_length=6, null=True, unique=True)
    session_date = models.DateField(auto_now=False)
    avalable_capacity =models.CharField(max_length=10, null=True)
    slot = models.CharField(max_length=20, null=True)


class Certificate(models.Model):
    VACCINE = (
        ('Covishield', 'Covishield'),
        ('Covaxin', 'Covaxin'),
    )
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.SET_NULL)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    dose = models.CharField(max_length=2, null=True)
    date_of_dose = models.DateField(auto_now=True)
    vaccine_name = models.CharField(max_length=50,null=True, choices=VACCINE)
    vaccinated_by = models.CharField(max_length=50)
