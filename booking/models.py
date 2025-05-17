from django.db import models
from django.utils.crypto import get_random_string
from services.models import Service

class Booking(models.Model):
    SLOT_CHOICES = [
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-13:00', '12:00-13:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
    ]

    id = models.CharField(max_length=30, primary_key=True, editable=False)

    customer_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_slot = models.CharField(max_length=20, choices=SLOT_CHOICES)
    services = models.ManyToManyField(Service)
    email_info = models.EmailField()
    contact_info = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_booking_id()
        super().save(*args, **kwargs)

    def generate_booking_id(self):
        date_str = self.appointment_date.strftime('%Y%m%d')
        time_str = self.appointment_slot.split('-')[0].replace(':', '')
        
        count = Booking.objects.filter(
            appointment_date=self.appointment_date,
        ).count() + 1

        return f"MAC-{date_str}-{time_str}-{count:03d}"


    def __str__(self):
        return self.id
