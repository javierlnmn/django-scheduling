from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone

from .models import Appointment, Holiday

class AppointmentForm(forms.ModelForm):
    
    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['token', 'token_expiry_date']

    def clean(self):
        cleaned_data = super().clean()

        appointment_date = cleaned_data.get('appointment_date')

        if appointment_date < timezone.now().date():
            raise ValidationError({'appointment_date': ['This date is not a valid date.']})

        is_holiday = Holiday.objects.filter(date=appointment_date).exists()
            
        if is_holiday:
            raise ValidationError({'appointment_date': ['This date is not a valid date.']})

        appointment_time = cleaned_data.get('appointment_time')

        existing_appointment = Appointment.objects.filter(
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exclude(pk=self.instance.pk if self.instance else None)

        if existing_appointment.exists():
            raise ValidationError({'appointment_time': ['This time is not available for your appointment.']})

        return cleaned_data
