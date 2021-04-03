from django import forms
from accounts.models import Beneficiary



class VaccinationStatusForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['email', 'first_name', 'dose1_status']