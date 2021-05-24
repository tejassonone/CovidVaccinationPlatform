from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from appointment.models import Appointment
from accounts.models import Beneficiary
import json, random, calendar
from datetime import *
from dateutil.relativedelta import *
from .models import Session
from django.utils.http import is_safe_url
from accounts.forms import RegisterForm, PersonalInfoForm, HealthInfoForm
from appointment.forms import AppointmentForm
from .forms import VaccinationStatusForm, CertificateForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from accounts.decorators import allowed_users
# Create your views here.
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required




def dashboard_view(request):
    for i in range(1, 13):
        get_date = date.today()
        print('month',calendar.month_abbr[i])
        vaccinated = Appointment.objects.filter(session_date__month=f'{i}', session_date__year=f'{get_date.year}').count()
        print('vaccinated',vaccinated)
        data.append({'month':calendar.month_abbr[i], 'vaccinated_count':vaccinated})

    for i in range(6, -1, -1):
        get_date = date.today() + relativedelta(days=-i)
        print('day',get_date.strftime("%a"))
        vaccinated = Appointment.objects.filter(session_date__day=f'{get_date.day}', session_date__month=f'{get_date.month}').count()
        print('vaccinated day',vaccinated)

    appointment =Appointment.objects.all()
    vaccinated = Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated'))
    sheduled = Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))
    qs = Appointment.objects.filter(session_date__range=["2021-04-22", "2022-01-31"])
    print('date-----',appointment.filter(session_date__range=["2021-04-22", "2022-01-31"]))
    total_appointment = appointment.count()
    total_sheduled = sheduled.count()
    total_vaccinated = vaccinated.count()
    context={'total_sheduled':total_sheduled, 'total_vaccinated':total_vaccinated, 'total_appointment':total_appointment, 'data':total_appointment}
    return render(request, 'session/dashboard.html', context)

def vaccination_form_view(request, pk, *args, **kwargs):
    appointment = Appointment.objects.get(appointment_id=pk)
    s_id = appointment.session_id
    session = Session.objects.get(session_id=s_id)
    beneficiary = Beneficiary.objects.get(id=appointment.beneficiary.id)
    form1=VaccinationStatusForm(instance=beneficiary)
    form2 = CertificateForm()
    dose = appointment.dose
    if dose == '1':
        dose_status = 'dose1_status'
    else:
        dose_status = 'dose2_status'
    if request.method == 'POST':
        form1=VaccinationStatusForm(data=request.POST, instance=beneficiary)
        form2=CertificateForm(data=request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('session_view')
    context = {
        'form':form1,
        'form2':form2,
        "beneficiary": beneficiary,
        "session":session,
        "dose":dose,
        "dose_status":dose_status
    }
    return render(request, "session/vaccination_form.html", context, status=200)



@login_required(login_url='admin_login')
@allowed_users(allowed_roles=['admin'])
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

    @method_decorator(login_required)
    @method_decorator(staff_member_required)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Appointment.objects.all()
        response = [{'beneficiary':x.beneficiary.first_name +" " + x.beneficiary.last_name, 'dose':x.dose, 'appointment_id':x.appointment_id, 'session_date':x.session_date, 'slot':x.slot} for x in qs]
        context["qs_json"] = json.dumps(list(response), default=str)
        return context


class VaccinatedListView(ListView):
    model = Appointment
    template_name = 'session/list.html'

    @method_decorator(login_required)
    @method_decorator(staff_member_required)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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

    @method_decorator(login_required)
    @method_decorator(staff_member_required)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs=Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))
        response = [{'beneficiary':x.beneficiary.first_name +" " + x.beneficiary.last_name, 'dose':x.dose, 'appointment_id':x.appointment_id, 'session_date':x.session_date, 'slot':x.slot} for x in qs]
        context["qs_json"] = json.dumps(list(response), default=str)
        return context



class DashboardView(ListView):
    template_name = 'session/dashboard.html'

    @method_decorator(login_required)
    @method_decorator(staff_member_required)  
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_count=Session.objects.all().count()
        appointment =Appointment.objects.all()
        vaccinated = Appointment.objects.filter(Q(beneficiary__dose1_status='Vaccinated') or Q(beneficiary__dose2_status='Vaccinated'))
        sheduled = Appointment.objects.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))
        total_appointment = appointment.count()
        total_sheduled = sheduled.count()
        total_vaccinated = vaccinated.count()
        month_data=[]
        day_data =[]
        for i in range(1, 13):
            get_date = date.today()
            count = Appointment.objects.filter(session_date__month=f'{i}', session_date__year=f'{get_date.year}').count()
            month_data.append({'month':calendar.month_abbr[i], 'vaccinated_count':count})
        for i in range(6, -1, -1):
            get_date = date.today() + relativedelta(days=-i)
            count = Appointment.objects.filter(session_date__day=f'{get_date.day}', session_date__month=f'{get_date.month}').count()
            day_data.append({'day':get_date.strftime("%a"), 'vaccinated_count':count}) 
        context["qs"] = month_data
        context['day_qs'] =day_data
        context['total_sheduled']=total_sheduled
        context['total_vaccinated']=total_vaccinated
        context['total_appointment']=total_appointment
        context['total_session']=session_count
        return context


@login_required(login_url='admin_login')
@allowed_users(allowed_roles=['admin'])
def personal_info_view(request, app_id, *args, **kwargs):
    appointment = Appointment.objects.get(appointment_id=app_id)
    username = appointment.beneficiary
    beneficiary = Beneficiary.objects.get(email= username)
    form1 = PersonalInfoForm(instance=beneficiary)
    context = {'form1':form1, 'app_id':app_id}   
    return render(request, 'session/beneficiary_detail/personal_info.html', context)

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=['admin'])
def health_info_view(request, app_id, *args, **kwargs):
    appointment = Appointment.objects.get(appointment_id=app_id)
    username = appointment.beneficiary
    beneficiary = Beneficiary.objects.get(email= username)
    form2 = HealthInfoForm(instance=beneficiary)
    context = {'form2':form2, 'app_id':app_id}   
    return render(request, 'session/beneficiary_detail/health_info.html', context)

@login_required(login_url='admin_login')
@allowed_users(allowed_roles=['admin'])
def vaccination_info_view(request, app_id, *args, **kwargs):
    appointment = Appointment.objects.get(appointment_id=app_id)
    username = appointment.beneficiary
    beneficiary = Beneficiary.objects.get(email= username)
    certificate = beneficiary.appointment_set.all()
    context={'appointment':certificate, 'app_id':app_id}
    return render(request, 'session/beneficiary_detail/vaccination_info.html', context)








