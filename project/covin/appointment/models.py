from django.db import models
from accounts.models import Beneficiary
from session.models import Session

# Create your models here.

class Appointment(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, null=True, on_delete=models.SET_NULL)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    dose = models.CharField(max_length=2, null=True)
    appointment_id = models.CharField(primary_key=True, max_length=20)
    session_date = models.CharField(max_length=20, null=True)
    slot = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
     

@property
def dose_status(self):
    if dose1_status =='Not-Sheduled':
        return '1'
    else:
        return '2'
        
