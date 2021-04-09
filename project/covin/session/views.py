from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from appointment.models import Appointment
from accounts.models import Beneficiary
import json
from accounts.forms import RegisterForm
from .forms import VaccinationStatusForm

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, "session/dashboard.html", context={}, status=200)


def vaccination_form_view(request, pk, *args, **kwargs):
    appointment = Appointment.objects.get(appointment_id=pk)
    qs = Beneficiary.objects.get(id=appointment.beneficiary.id)
    form=VaccinationStatusForm(instance=qs)
    if request.method == 'POST':
        form=VaccinationStatusForm(data=request.POST, instance=qs)
        print('form save------',request.POST)
        if form.is_valid():
            form.save()
            return redirect('session_view')
    context = {
        'form':form,
        "qs": qs
    }
    return render(request, "session/vaccination_form.html", context, status=200)



def session_view(request):
    appointment =Appointment.objects.all()
    not_seduled = Appointment.objects.filter(beneficiary__dose1_status='Not-Sheduled')
    vaccinated = Appointment.objects.filter(beneficiary__dose1_status='Vaccinated')
    sheduled = Appointment.objects.filter(beneficiary__dose1_status='Sheduled')

    total_appointment = appointment.count
    total_sheduled = sheduled.count()
    total_vaccinated = vaccinated.count()
    context={'sheduled':sheduled, 'vaccinated':vaccinated, 'total_appointment':total_appointment, 'total_sheduled':total_sheduled, 'total_vaccinated':total_vaccinated, 'appointment':appointment}
    return render(request, 'session/session.html', context)
















def list_view(request, *args, **kwargs):
    qs = Appointment.objects.all()
    print("QS",qs)
    list = [{"id": x.appointment_id , "name": x.beneficiary.first_name, "appointment_date":x.session_date} for x in qs]
    data = {
        "isUser": False,
        "response": list
    }
    return JsonResponse(data)




def vaccination_form_save(request, *args, **kwargs):
    qs = Beneficiary.objects.get(id=7)
    form=RegisterForm(initial={'Beneficiary':qs})
    return render(request, "session/form_save.html", {'form':form}, status=200)



def form_save(request, *args, **kwargs):
    qs = Beneficiary.objects.get(id=7)
    form=VaccinationStatusForm(instance=qs)
    if request.method == 'POST':
        form=VaccinationStatusForm(data=request.POST, instance=qs)
        if form.is_valid():
            form.save()
            return redirect('session_view')
    return render(request, "session/form_save.html", {'form':form}, status=200)



