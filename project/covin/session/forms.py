from django import forms
from accounts.models import Beneficiary
from .models import Certificate

class VaccinationStatusForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['email', 'first_name', 'dose1_status']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['beneficiary', 'session', 'dose', 'vaccine_name', 'vaccinated_by']