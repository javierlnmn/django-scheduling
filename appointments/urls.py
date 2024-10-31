from django.urls import path
import appointments.views as views

app_name="appointments"

urlpatterns = [
    path('', views.AppointmentFormView.as_view(), name="appointment_form"),
    path('appointment-confirmation/<str:submission_token>/', views.AppointmentConfirmationView.as_view(), name='appointment_confirmation_page'),
    path('available-times/', views.available_times, name="available_time"),
]
