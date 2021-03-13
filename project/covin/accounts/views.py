from django.shortcuts import render, redirect
from .forms import BeneficiaryInfoForm

# Create your views here.

def home(request):
    return HttpResponse('hello')


def register(request):
    if request.method == 'POST':
        form = BeneficiaryInfoForm(request.POST)
        if form.is_valid():
            print("registered succesfully------------------")
    form = BeneficiaryInfoForm()
    return render(request, 'accounts/multistep_register.html', {'form':form})

