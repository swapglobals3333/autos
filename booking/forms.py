from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'appointment_date', 'appointment_slot', 'services', 'contact_info', 'email_info']
        labels = {
            'customer_name': 'Name',
            'services': 'Select services',
            'contact_info': 'Contact number',
            'email_info': 'Email address',
        }

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_slot': forms.Select(),
            'services': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

        # Set 'min' attribute to today to prevent past dates
        self.fields['appointment_date'].widget.attrs['min'] = date.today().isoformat()

        for name, field in self.fields.items():
            field.widget.attrs.update()

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < date.today():
            raise forms.ValidationError("Please select a future date.")
        return appointment_date


class DeleteBookingForm(forms.Form):
    booking_id = forms.CharField(
        label="Booking ID",
        max_length=30,  # Adjust length as needed
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., MAC-20250601-0900-001'
        })
    )

    def __init__(self, *args, **kwargs):
        super(DeleteBookingForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

