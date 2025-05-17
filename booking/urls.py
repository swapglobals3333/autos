from django.urls import path
from . import views


urlpatterns = [
    path('', views.booking_home, name='booking-home'),
    path('new-booking/', views.new_booking, name='new-booking'),
    path('confirm-booking/', views.confirmBooking, name='confirm-booking'),
    path('modify-booking/', views.modify_booking, name='modify-booking'),
    path('cancel-booking/', views.cancel_booking, name='cancel-booking'),
]