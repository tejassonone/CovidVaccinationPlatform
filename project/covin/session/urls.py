from django.urls import path
from . import views

urlpatterns = [
    path('dash', views.dashboard_view, name='dash'),
    path('vaccination_form/<str:pk>/', views.vaccination_form_view, name='vaccination_form'),
    path('vaccination_form_save/', views.vaccination_form_save, name='vaccination_form_save'),
    path('form_save/', views.form_save, name='form_save'),
    path('session_view/', views.session_view, name='session_view'),


    path('appointment_list_view/', views.AppointmentListView.as_view(), name='appointment_list_view'),
    path('vaccinated_list_view/', views.VaccinatedListView.as_view(), name='vaccinated_list_view'),
    path('pending_list_view/', views.PendingListView.as_view(), name='pending_list_view'),
    path('', views.DashboardView.as_view(), name='dashboard_view'),

    path('personal_info_view/<str:app_id>/', views.personal_info_view, name='personal_info_view'),
    path('health_info_view/<str:app_id>/', views.health_info_view, name='health_info_view'),
    path('vaccination_info_view/<str:app_id>/', views.vaccination_info_view, name='vaccination_info_view'),



]