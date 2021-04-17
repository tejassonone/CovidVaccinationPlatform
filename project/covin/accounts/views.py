from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, PersonalInfoForm, HealthInfoForm
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Beneficiary, User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib import messages

# Create your views here.

@unauthenticated_user
def register(request, *args, **kwargs):
    next_post = request.POST.get('next')
    redirect_path = next_post or None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            first_name = form.cleaned_data.get('first_name')

            group = Group.objects.get(name='beneficiary')
            user.groups.add(group)
            messages.success(request, 'Account was created for' + first_name)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("login")
    else:
        form = RegisterForm()
    return render(request, 'accounts/multistep_register.html', {'form':form})


@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
        'user_type':'Beneficiary'
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
            messages.info(request, 'Email OR password is incorrect')
            return render(request, "accounts/login.html", context)
    return render(request, "accounts/login.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def profile(request):
    username = request.user
    qs = Beneficiary.objects.get(email=username)
    context ={
        'user':qs,
    } 
    return render(request, 'accounts/profile_page.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def update_personal_info(request):
    username = request.user
    qs = Beneficiary.objects.get(email=username)
    form1 = PersonalInfoForm(instance=qs)
    context = {'form1':form1}
    next_post = request.POST.get('next')
    redirect_path = next_post or None
    if request.method=='POST':
        form1 = PersonalInfoForm(request.POST, instance=qs)
        if form1.is_valid():
            form1.save()
            if is_safe_url(redirect_path, request.get_host()):
                print('run1')
                return redirect(redirect_path)
            else:
                return redirect("/")    
    return render(request, 'accounts/personal_info_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def update_health_info(request):
    username = request.user
    qs = Beneficiary.objects.get(email=username)
    form2 = HealthInfoForm(instance=qs)
    context = {'form2':form2}
    next_post = request.POST.get('next')
    redirect_path = next_post or None
    if request.method=='POST':
        form2 = HealthInfoForm(request.POST, instance=qs)
        if form2.is_valid():
            form2.save()
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")    
    return render(request, 'accounts/health_info_form.html', context)






def about(request):
    context = {}
    return render(request, 'accounts/about.html', context)







def register1(request):
    form=RegisterForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['beneficiary'])
def is_email_already_exist(request, *args, **kwargs):
    email = request.GET.get('email')
    if Beneficiary.objects.filter(email=email).exists():
        user_exist=True
    else:
        user_exist=False
    return JsonResponse({'userExist':user_exist})




#-----------admin login ------------------#

@unauthenticated_user
def admin_login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
        'user_type':'Admin'
    }
    if form.is_valid():
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            messages.info(request, 'Email OR password is incorrect')
            return render(request, "accounts/login.html", context)
    return render(request, "accounts/login.html", context)