from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from appointment.models import Appointment
from accounts.models import Beneficiary
import json
from accounts.forms import RegisterForm
from .forms import VaccinationStatusForm
from django.db.models import Q
# Create your views here.
from django.views.generic import ListView


def dashboard_view(request):
    appointment =Appointment.objects.all()
    vaccinated = Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated'))
    sheduled = Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))

    total_appointment = appointment.count()
    total_sheduled = sheduled.count()
    total_vaccinated = vaccinated.count()
    context={'total_sheduled':total_sheduled, 'total_vaccinated':total_vaccinated, 'total_appointment':total_appointment}
    return render(request, 'session/dashboard.html', context)

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
    vaccinated = Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated'))
    sheduled = Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))

    total_appointment = appointment.count()
    total_sheduled = sheduled.count()
    total_vaccinated = vaccinated.count()
    context={'sheduled':sheduled, 'vaccinated':vaccinated, 'total_appointment':total_appointment, 'total_sheduled':total_sheduled, 'total_vaccinated':total_vaccinated, 'appointment':appointment}
    return render(request, 'session/session.html', context)




class AppointmentListView(ListView):
    model = Appointment
    template_name = 'session/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Appointment.objects.all()
        response = [{'beneficiary':x.beneficiary.first_name +" " + x.beneficiary.last_name, 'dose':x.dose, 'appointment_id':x.appointment_id, 'session_date':x.session_date, 'slot':x.slot} for x in qs]
        context["qs_json"] = json.dumps(list(response), default=str)
        return context

class VaccinatedListView(ListView):
    model = Appointment
    template_name = 'session/list.html'

    def get_queryset(self):
        return Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated')) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated'))
        response = [{'beneficiary':x.beneficiary.first_name +" " + x.beneficiary.last_name, 'dose':x.dose, 'appointment_id':x.appointment_id, 'session_date':x.session_date, 'slot':x.slot} for x in qs]
        context["qs_json"] = json.dumps(list(response), default=str)
        return context

class PendingListView(ListView):
    model = Appointment
    template_name = 'session/list.html'

    def get_queryset(self):
        return Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))
        response = [{'beneficiary':x.beneficiary.first_name +" " + x.beneficiary.last_name, 'dose':x.dose, 'appointment_id':x.appointment_id, 'session_date':x.session_date, 'slot':x.slot} for x in qs]
        context["qs_json"] = json.dumps(list(response), default=str)
        return context




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



