from django.shortcuts import render
from django.http import JsonResponse
from vaccine_centre.models import VaccineCentre

# Create your views here.

def appointment_view(request):
    return render(request, 'appointment/appointment_page.html')



def filter_centre(request):
    state = [ "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry"]
    state_list =[{'state':x} for x in state]
    context ={
        'qs':state_list,
    }
    return render(request, 'appointment/filter_centre.html' ,context)


def get_json_state_data(request):
    qs_value_state = [ "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Delhi","Lakshadweep","Puducherry"]
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
