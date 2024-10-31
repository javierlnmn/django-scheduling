from django.apps import apps
from django import forms
from django.contrib import admin
from appointments.models import (
    Holiday,
    WeekDay,
    AppointmentTime,
    Appointment
)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'appointment_date', 'appointment_time')
    list_filter = ('name', 'surname', 'appointment_date')
    search_fields = ('name', 'surname')
    exclude = ('token', 'token_expiry_date')
    
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ('name', 'date')
    search_fields = ('name', 'date')

class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

class AppointmentTimeAdmin(admin.ModelAdmin):
    list_display = ('time', 'week_days_display')
    list_filter = ('time',)
    search_fields = ('time', 'week_days')

    def week_days_display(self, obj):
        week_days = [day.get_name_display() for day in obj.week_days.all()]
        return ((', ').join(week_days))


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(AppointmentTime, AppointmentTimeAdmin)
