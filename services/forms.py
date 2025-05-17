from django.forms import ModelForm
from .models import Service
from django import forms

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class EstimateForm(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple,
        required=True
    )
    estimated_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0.00)
