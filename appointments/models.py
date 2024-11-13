from django.db import models
from django.utils import timezone
from common.utils import generate_unique_token
from accounts.models import CustomUser

from datetime import datetime
import calendar

DAYS_WEEK = [(i, list(calendar.day_name)[i]) for i in range(len(list(calendar.day_name)))]

class Holiday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return self.name


class WeekDay(models.Model):
    name = models.IntegerField(unique=True, choices=DAYS_WEEK)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Week Days Available for Appointments'
        verbose_name_plural = 'Week Days Available for Appointments'


class AppointmentTime(models.Model):
    time = models.TimeField(max_length=8)
    week_days = models.ManyToManyField(WeekDay)

    def __str__(self):
        return self.time.strftime('%H:%M')

    class Meta:
        verbose_name = 'Available Times for Appointments'
        verbose_name_plural = 'Available Times for Appointments'


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=25)
    email = models.EmailField(max_length=255)
    appointment_date = models.DateField()
    appointment_time = models.ForeignKey(AppointmentTime, on_delete=models.PROTECT)
    appointment_created_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    token = models.CharField(max_length=100, default=generate_unique_token, unique=True)
    token_expiry_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.token_expiry_date:
            self.token_expiry_date = self.appointment_date
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} {self.surname}'s appointment on {self.appointment_date} at {self.appointment_time}"
    
    class meta:
        ordering = ('-appointment_date', '-appointment_time')
    
    @staticmethod
    def get_available_times(date):
        
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        is_holiday = Holiday.objects.filter(date=date).exists()
        is_today = timezone.now().date() == parsed_date
        now = timezone.now()
            
        if is_holiday:
            available_times = []
            return available_times
            
        day_of_week = parsed_date.weekday()

        if is_today:
            all_times = AppointmentTime.objects.filter(week_days__name=day_of_week, time__gt=now)
        else:
            all_times = AppointmentTime.objects.filter(week_days__name=day_of_week)
        
        existing_appointments = Appointment.objects.filter(appointment_date=date).values_list('appointment_time__time', flat=True)

        available_times = [{
            'time_label': appointment_time.time.strftime('%H:%M'),
            'time_value': appointment_time.id,
        } for appointment_time in all_times if appointment_time.time not in existing_appointments]

        return available_times
