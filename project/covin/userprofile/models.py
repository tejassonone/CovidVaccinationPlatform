from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    DOSE_STATUS = (
        ('Sheduled', 'Sheduled'),
        ('Not-Sheduled', 'Not-Sheduled'),
        ('Vaccinated', 'Vaccinated')
    )

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=200, null=True  )
    last_name = models.CharField(max_length=200, null=True)
    year_of_birth = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    mobile_no = models.CharField(max_length=200, null=True)
    dose1_status = models.CharField(max_length=200, null=True, choices=DOSE_STATUS)
    dose2_status = models.CharField(max_length=200, null=True, choices=DOSE_STATUS)

    def __str__(self):
        return self.first_name

