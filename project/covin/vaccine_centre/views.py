from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    context={}
    return render(request, 'vaccine_centre/main.html', context)

