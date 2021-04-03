from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='session_home'),
    path('list_view/', views.list_view, name='list_view'),
    path('vaccination_form/<str:pk>/', views.vaccination_form_view, name='vaccination_form'),
    path('vaccination_form_save/', views.vaccination_form_save, name='vaccination_form_save'),
    path('form_save/', views.form_save, name='form_save'),
    path('session_view/', views.session_view, name='session_view'),



]