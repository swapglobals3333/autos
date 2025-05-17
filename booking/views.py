from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from .forms import BookingForm, DeleteBookingForm
from .models import Booking
from services.models import Service
from datetime import datetime, timedelta
from datetime import datetime


def booking_home(request):
    return render(request, 'booking/booking_home.html')

def new_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Validate date and slot logic
            appointment_date = form.cleaned_data['appointment_date']
            appointment_slot = form.cleaned_data['appointment_slot']
            services = form.cleaned_data['services']

            if appointment_date < timezone.now().date():
                messages.error(request, "You cannot book an appointment for a past date.")
                return render(request, 'booking_form.html', {'form': form})

            existing_bookings = Booking.objects.filter(
                appointment_date=appointment_date,
                appointment_slot=appointment_slot
            )
            if existing_bookings.count() >= 2:
                messages.error(request, "This slot already has 2 bookings. Please choose another slot.")
                return render(request, 'booking_form.html', {'form': form})

            # Temporarily store form data in session
            request.session['temp_booking_data'] = {
                'customer_name': form.cleaned_data['customer_name'],
                'contact_info': form.cleaned_data['contact_info'],
                'email_info': form.cleaned_data['email_info'],
                'appointment_date': str(appointment_date),
                'appointment_slot': appointment_slot,
                'services': [service.id for service in services]
            }
            return redirect('confirm-booking')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})


def confirmBooking(request):
    temp_data = request.session.get('temp_booking_data')

    if not temp_data:
        messages.error(request, "No booking data found.")
        return redirect('new-booking')

    # Get actual service objects from IDs stored in session
    services = Service.objects.filter(id__in=temp_data['services'])
    total_price = sum(service.price for service in services)

    if request.method == 'POST':
        # Create and save booking
        appointment_date = datetime.strptime(temp_data['appointment_date'], '%Y-%m-%d').date()
        booking = Booking.objects.create(
            customer_name=temp_data['customer_name'],
            contact_info=temp_data['contact_info'],
            email_info=temp_data['email_info'],
            appointment_date=appointment_date,
            appointment_slot=temp_data['appointment_slot'],
            total_price=total_price
        )
        booking.services.set(services)

        # Clear session
        request.session.pop('temp_booking_data', None)

        messages.success(request, "Booking confirmed!")
        return redirect('booking-home')

    context = {
        'booking': temp_data,
        'services': services,
        'total_price': total_price
    }
    return render(request, 'booking/confirm_booking.html', context)



def cancel_booking(request):
    if request.method == 'POST':
        form = DeleteBookingForm(request.POST)
        if form.is_valid():
            booking_id = form.cleaned_data['booking_id'].strip().upper()
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.delete()
                messages.success(request, f"Booking with ID '{booking_id}' has been cancelled successfully.")
                return redirect('booking-home')

            except Booking.DoesNotExist:
                messages.error(request, f"No booking found with ID '{booking_id}'. Please check the ID and try again.")
    else:
        form = DeleteBookingForm()

    return render(request, 'booking/cancel_booking.html', {'form': form})


def modify_booking(request):
    booking = None
    form = None

    if request.method == 'POST':
        if 'booking_id' in request.POST: 
            booking_id = request.POST.get('booking_id')
            try:
                booking = Booking.objects.get(id=booking_id)
                form = BookingForm(instance=booking)
            except Booking.DoesNotExist:
                messages.error(request, 'Booking not found.')
                form = None

        elif 'id' in request.POST:  
            booking_id = request.POST.get('id')
            try:
                booking = Booking.objects.get(id=booking_id)
                form = BookingForm(request.POST, instance=booking)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Booking updated successfully.')
                    return redirect('booking-home')
            except Booking.DoesNotExist:
                messages.error(request, 'Booking not found.')

    return render(request, 'booking/modify_booking.html', {'form': form, 'booking': booking})
