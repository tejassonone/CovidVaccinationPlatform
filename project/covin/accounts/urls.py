from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('is_email_already_exist/', views.is_email_already_exist, name='is_email_already_exist'),
    path('update_personal_info/', views.update_personal_info, name='update_personal_info'),
    path('update_health_info/', views.update_health_info, name='update_health_info'),

    path('certificate/', views.certificate_view, name='certificate_view'),

    path('about/', views.about, name='about'),

    path('register1/', views.register1, name='register1'),

]