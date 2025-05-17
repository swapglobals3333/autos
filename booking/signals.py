from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .models import Booking

@receiver(post_save, sender=Booking)
def booking_confirmation_mail(sender, instance, created, **kwargs):
    if created:
        booking = instance

        subject = "Maple Auto Care: Booking Confirmation"
        message = f"""Dear {booking.customer_name},

        Your booking (ID: {booking.id}) has been confirmed. 
        Here are your booking details:

        Appointment Date: {booking.appointment_date}
        Appointment Time: {booking.appointment_slot}

        Estimated Price: {booking.total_price}

        Thank you for choosing Maple Auto Care.
        We look forward to serving you!

        Best regards,  
        Maple Auto Care Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.email_info],
            fail_silently=False,
        )

        # try:
        #     phone = booking.contact_info.strip()

        #     # Ensure E.164 format
        #     if not phone.startswith('+'):
        #         phone = '+91' + phone[-10:]

        #     print(phone)
        #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        #     whatsapp_message = client.messages.create(
        #         body=message,
        #         from_=settings.TWILIO_WHATSAPP_NUMBER,
        #         to=f"whatsapp:{phone}"
        #     )
        # except Exception as e:
        #     print(f"Error sending WhatsApp message: {e}")
