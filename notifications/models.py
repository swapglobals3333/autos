from django.db import models
from booking.models import Booking

class Notification(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, related_name='notifications', null=True, blank=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.channel.upper()} to {self.booking.customer_name} on {self.sent_at.date()}"