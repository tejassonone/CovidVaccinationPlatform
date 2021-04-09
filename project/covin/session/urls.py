from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('vaccination_form/<str:pk>/', views.vaccination_form_view, name='vaccination_form'),
    path('vaccination_form_save/', views.vaccination_form_save, name='vaccination_form_save'),
    path('form_save/', views.form_save, name='form_save'),
    path('session_view/', views.session_view, name='session_view'),


    path('appointment_list_view/', views.AppointmentListView.as_view(), name='appointment_list_view'),
    path('vaccinated_list_view/', views.VaccinatedListView.as_view(), name='vaccinated_list_view'),
    path('pending_list_view/', views.PendingListView.as_view(), name='pending_list_view')

]