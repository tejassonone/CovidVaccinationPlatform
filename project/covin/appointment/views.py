import random, json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from vaccine_centre.models import VaccineCentre
from accounts.models import Beneficiary
from session.models import Session
from .forms import AppointmentForm, BeneficiaryForm
from .models import Appointment
from django.contrib.auth.decorators import login_required
from accounts.decorators import unauthenticated_user, allowed_users
from datetime import *
from django.db.models import Q

from dateutil.relativedelta import *
# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def appointment_view(request):
    return render(request, 'appointment/appointment_page.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def filter_centre(request):
    context ={
    }
    return render(request, 'appointment/filter_centre.html' ,context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def get_json_state_data(request):
    qs_value = list(VaccineCentre.objects.values('state_name').distinct())
    return JsonResponse({'data':qs_value})


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def get_json_district_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    obj_dist = list(VaccineCentre.objects.filter(state_name=selected_state).values('district_name').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def get_json_block_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    selected_district = kwargs.get('district')
    obj_dist = list(VaccineCentre.objects.filter(district_name=selected_district, state_name=selected_state).values('block_name').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def get_json_pincode_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    selected_district = kwargs.get('district')
    selected_block = kwargs.get('block')
    obj_dist = list(VaccineCentre.objects.filter(block_name=selected_block, district_name=selected_district, state_name=selected_state).values('pincode').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)



@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def filter_view(request):
    if request.is_ajax():
        state = request.GET.get('state_name')
        district = request.GET.get('district_name')
        block = request.GET.get('block_name')
        pincode = request.GET.get('pincode')
        qs = VaccineCentre.objects.filter(state_name=state, district_name=district, block_name=block, pincode=pincode).values()
        centre_data = []
        for row in qs:
            centre = VaccineCentre.objects.get(centre_id=row['centre_id'])
            sessions = centre.session_set.all()
            date_data = []
            for i in range(1, 29):
                get_date = date.today() + relativedelta(days=i)
             
                session = Session.objects.filter(session_date__day=f'{get_date.day}', session_date__month=f'{get_date.month}', centre=centre).first()
                if session:
                    availability = session.avalable_capacity
                    s_id = session.session_id
                    beneficiary = Beneficiary.objects.get(email=request.user)
                    app = Appointment.objects.filter(session=session, beneficiary=beneficiary)
                    if app:
                        action='Booked'
                    else:
                        action='Book'
                else:
                    availability = 0
                    s_id = 0
                    action='NA'
                date_data.append({'date':get_date.strftime("%d %b "), 'session_id':s_id, 'v_count':availability, 'action':action})
            centre_data.append({'centre_id':row['centre_id'], 'centre_name':row['centre_name'], 'session':date_data})
        return JsonResponse({'data':list(centre_data)})
    return JsonResponse({'data':'not dones'})



@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def centre_detail(request, s_id):
    if request.is_ajax():
        beneficiary = Beneficiary.objects.get(email=request.user)
        session_obj = Session.objects.filter(session_id=s_id)
        centre_obj = Session.objects.get(session_id=s_id).centre
        print('centre_detail',centre_obj)
        if beneficiary.dose1_status == 'Not-Sheduled':
            value1='Sheduled'
            value2 = beneficiary.dose2_status
            dose='1'
        elif beneficiary.dose2_status == 'Not-Sheduled' and beneficiary.dose1_status != 'Not-Sheduled':
            dose2_status = 'dose2_status'
            value1 = beneficiary.dose1_status
            value2 ='Sheduled'
            dose='2'
        else:
            value1=""
            value2=""
            dose=""
            
        qs = [{'centre_name':centre_obj.centre_name, 'block':centre_obj.block_name, 'session_id':x.session_id, 'session_date':x.session_date, 'slot':x.slot} for x in session_obj]
        return JsonResponse({'data':list(qs)})
    return JsonResponse({'data':'not dones'})


def create_appointment_view(request, s_id):
    action = request.GET.get('action')
    beneficiary = Beneficiary.objects.get(email=request.user)
    session_obj = Session.objects.filter(session_id=s_id).first()
    s_date=session_obj.session_date
    s_slot = session_obj.slot
    if beneficiary.dose1_status == 'Not-Sheduled':
        value1='Sheduled'
        value2 = beneficiary.dose2_status
        dose='1'
    elif beneficiary.dose2_status == 'Not-Sheduled' and beneficiary.dose1_status != 'Not-Sheduled':
        value1 = beneficiary.dose1_status
        value2 ='Sheduled'
        dose='2'
    else:
        value1=""
        value2=""
        dose=""
        return render(request, 'appointment/book_appointment.html', context)
    if action == 'book':
        beneficiary.dose1_status = value1
        beneficiary.dose2_status = value2
        beneficiary.save()
        obj = Appointment.objects.create(beneficiary=beneficiary, session=session_obj, dose=dose, appointment_id=random.randint(0, 100000), session_date=s_date, slot=s_slot)
        return redirect('profile')
    return JsonResponse({})

@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def book_appointment(request, id, *args, **kwargs):
    print('run--')
    centre = VaccineCentre.objects.get(centre_id=id)
    sessions = centre.session_set.all()
    beneficiary = Beneficiary.objects.get(email=request.user)
    form = BeneficiaryForm(instance=beneficiary)
    if beneficiary.dose1_status == 'Not-Sheduled':
        value1='Sheduled'
        value2 = beneficiary.dose2_status
        dose='1'
    elif beneficiary.dose2_status == 'Not-Sheduled' and beneficiary.dose1_status != 'Not-Sheduled':
        dose2_status = 'dose2_status'
        value1 = beneficiary.dose1_status
        value2 ='Sheduled'
        dose='2'
    else:
        value1=""
        value2=""
        dose=""
        messages.info(request, 'You have already registered for dose1 and dose2')
        return render(request, 'appointment/book_appointment.html', context)
    if request.method=='POST':
        app_form=AppointmentForm(request.POST)
        user_form=BeneficiaryForm(request.POST, instance=beneficiary)
        print('post------',request.POST)
        if app_form.is_valid() and user_form.is_valid():
            app_obj=app_form.save(commit=False)
            user_obj=form.save(commit=False)
           # app_obj.save()
           # user_obj.save()
            print('book')
            return redirect('profile')
    context ={
        'qs':centre,
        'sessions':sessions,
        'beneficiary':beneficiary,
        'dose':dose,
        'appointment_id':random.randint(0, 100000),
        'form':form,
        'value1':value1,
        'value2':value2
    }
    return render(request, 'appointment/filter_centre.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def booked_appointment(request,*args, **kwargs):
    beneficiary = Beneficiary.objects.get(email=request.user)
    appointment = Appointment.objects.filter(beneficiary=beneficiary)
    app = appointment.filter(Q(beneficiary__dose1_status='Sheduled') or Q(beneficiary__dose2_status='Sheduled'))
    context ={
        'appointment':app
    }
    return render(request, 'appointment/booked_appointment.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def delete_appointment(request, id, *args, **kwargs):
    appointment =Appointment.objects.get(appointment_id=id)
    if request.method=='POST':
        appointment.delete()
        return redirect('booked_appointment')
    context ={ }
    return render(request, 'appointment/delete_appointment.html', context)   
 








def book_action_view(request):
    beneficiary = Beneficiary.objects.get(email=request.user)
    app_form = AppointmentForm()
    dose='3'
    if beneficiary.dose1_status == 'Not-Sheduled':
        value1='Sheduled'
        value2 = beneficiary.dose2_status
        dose='1'
    elif beneficiary.dose2_status == 'Not-Sheduled' and beneficiary.dose1_status != 'Not-Sheduled':
        dose2_status = 'dose2_status'
        value1 = beneficiary.dose1_status
        value2 ='Sheduled'
        dose='2'
    else:
        value1=""
        value2=""
        dose=""
    if request.method=='POST':
        pass
    context ={'dose':dose}
    return render(request, 'appointment/book_appointment.html', context)




def filter_map_view(request):
    if request.is_ajax():
        c_id = request.GET.get('centre_id')
        qs = VaccineCentre.objects.filter(centre_id=c_id).values()
        centre_data = []
        for row in qs:
            centre = VaccineCentre.objects.get(centre_id=row['centre_id'])
            sessions = centre.session_set.all()
            date_data = []
            for i in range(1, 29):
                get_date = date.today() + relativedelta(days=i)
             
                session = Session.objects.filter(session_date__day=f'{get_date.day}', session_date__month=f'{get_date.month}', centre=centre).first()
                if session:
                    availability = session.avalable_capacity
                    s_id = session.session_id
                    beneficiary = Beneficiary.objects.get(email=request.user)
                    app = Appointment.objects.filter(session=session, beneficiary=beneficiary)
                    if app:
                        action='Booked'
                    else:
                        action='Book'
                else:
                    availability = 0
                    s_id = 0
                    action='NA'
                date_data.append({'date':get_date.strftime("%d %b "), 'session_id':s_id, 'v_count':availability, 'action':action})
            centre_data.append({'centre_id':row['centre_id'], 'centre_name':row['centre_name'], 'session':date_data})
        return JsonResponse({'data':list(centre_data)})
    return JsonResponse({'data':'not dones'})
    return JsonResponse({'data':'not dones'})