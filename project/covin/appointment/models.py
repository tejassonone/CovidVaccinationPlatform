from django.db import models

# Create your models here.

class Appointment(models.Model):
    centre_id = models.CharField(max_length=50)
    centre_name = models.CharField(max_length=200)
    state_name= models.CharField(max_length=200)
    district_name= models.CharField(max_length=200)
    block_name = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    
    dose = models.CharField(max_length=2)
    appointment_id = models.CharField(max_length=20)
    session_date = models.CharField(max_length=20)
    slot = models.CharField(max_length=50)
     
