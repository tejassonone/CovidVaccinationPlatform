from django import forms
from .models import Appointment
from accounts.models import Beneficiary

class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields = ['beneficiary', 'session','dose', 'appointment_id', 'session_date', 'slot']

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model=Beneficiary
        fields = ['dose1_status', 'dose2_status']