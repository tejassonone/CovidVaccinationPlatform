from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointment_view, name='appointment'),
    path('book_appointment/<int:id>/', views.book_appointment, name='book_appointment'),
    path('filter/', views.filter_centre, name='filter_centre'),
    path('state-json/', views.get_json_state_data, name='state-json'),
    path('district-json/<str:state>/', views.get_json_district_data, name='district-json'),
    path('block-json/<str:state>/<str:district>/', views.get_json_block_data, name='block-json'),
    path('block-json/<str:state>/<str:district>/<str:block>/', views.get_json_pincode_data, name='pincode-json'),
    path('search/', views.filter_view, name='search'),
    path('centre-detail/<str:s_id>/', views.centre_detail, name='centre-detail'),
    path('book_appointment_view/', views.book_action_view, name='book_appointment_view'),
    path('booked_appointment/', views.booked_appointment, name='booked_appointment'),
    path('delete_appointment/<int:id>/', views.delete_appointment, name='delete_appointment'),

    path('create_appointment/<str:s_id>/', views.create_appointment_view, name='create_appointment_view'),

    path('filter_map/', views.filter_map_view, name='filter_map'),


]