import random, json
from django.shortcuts import render
from django.http import JsonResponse
from vaccine_centre.models import VaccineCentre
from accounts.models import Beneficiary
from session.models import Session
from .forms import AppointmentForm
from .models import Appointment

# Create your views here.

def appointment_view(request):
    return render(request, 'appointment/appointment_page.html')



def filter_centre(request):
    context ={
    }
    return render(request, 'appointment/filter_centre.html' ,context)


def get_json_state_data(request):
    qs_value = list(VaccineCentre.objects.values('state_name').distinct())
    return JsonResponse({'data':qs_value})



def get_json_district_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    obj_dist = list(VaccineCentre.objects.filter(state_name=selected_state).values('district_name').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)


def get_json_block_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    selected_district = kwargs.get('district')
    obj_dist = list(VaccineCentre.objects.filter(district_name=selected_district, state_name=selected_state).values('block_name').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)


def get_json_pincode_data(request, *args, **kwargs):
    selected_state = kwargs.get('state')
    selected_district = kwargs.get('district')
    selected_block = kwargs.get('block')
    obj_dist = list(VaccineCentre.objects.filter(block_name=selected_block, district_name=selected_district, state_name=selected_state).values('pincode').distinct())
    data = {
        'data':obj_dist
    }
    return JsonResponse(data)

def filter_view(request):
    if request.is_ajax():
        state = request.GET.get('state_name')
        district = request.GET.get('district_name')
        block = request.GET.get('block_name')
        pincode = request.GET.get('pincode')
        qs = list(VaccineCentre.objects.filter(state_name=state, district_name=district, block_name=block, pincode=pincode).values())
        return JsonResponse({'data':qs})
    return JsonResponse({'data':'not dones'})





def book_appointment(request, id, *args, **kwargs):
    centre = VaccineCentre.objects.get(centre_id=id)
    sessions = centre.session_set.all()
    context ={
        'qs':centre,
        'sessions':sessions,
    }
    return render(request, 'appointment/book_appointment.html', context)



  
 



def book_action_view(request):
    s_id = request.GET.get("session_id")
    s_date = request.GET.get("session_date")
    s_slot = request.GET.get("slot")
    action = request.GET.get("action")
    qs = Session.objects.get(session_id=s_id)
    s_date =qs.session_date
    s_slot = qs.slot
    beneficiary = Beneficiary.objects.get(email=request.user)
    print("status",beneficiary.dose1_status)
    if beneficiary.dose1_status == 'Not-Sheduled':
        dose='1'
    else:
        dose='2' 
    if action == "book":
        new_book = Appointment.objects.create(
            beneficiary=beneficiary, 
            session=qs,
            dose=dose,
            appointment_id=random.randint(0, 100000),
            session_date=s_date,
            slot=s_slot,
                )
        return JsonResponse({}, status=201)
    return JsonResponse({}, status=200)