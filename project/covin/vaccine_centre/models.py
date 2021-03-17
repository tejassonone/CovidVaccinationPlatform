from django.db import models

# Create your models here.

class VaccineCentre(models.Model):
    FEE_TYPE = (
        ('Free', 'Free'),
        ('Paid', 'Paid'),
        )
    centre_id = models.CharField(max_length=10, null=True)
    centre_name = models.CharField(max_length=200, null=True)
    state_name = models.CharField(max_length=200, null=True)
    district_name = models.CharField(max_length=200, null=True)
    block_name = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=10, null=True)
    timing_from = models.CharField(max_length=20)
    timing_to = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=50, null=True, choices=FEE_TYPE)


