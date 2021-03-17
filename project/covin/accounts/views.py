from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse
from django.utils.http import is_safe_url

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Beneficiary, User

# Create your views here.


def register(request, *args, **kwargs):
    next_post = request.POST.get('next')
    redirect_path = next_post or None
    print("REDIRECT PATH", redirect_path)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("login")
    else:
        form = RegisterForm()
    return render(request, 'accounts/multistep_register.html', {'form':form})


def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_post = request.POST.get('next')
    redirect_path = next_post or None
    if form.is_valid():
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Error")
    return render(request, "accounts/login.html", context)



def home(request):
    username = request.user
    qs = Beneficiary.objects.get(email=username)
    print(qs)
    context ={
        'user':qs,
    } 
    return render(request, 'accounts/profile_page.html', context)