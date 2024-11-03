from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.conf import settings

from appointments.forms import AppointmentForm
from appointments.models import Appointment

import json

class AppointmentFormView(FormView):
    template_name = 'appointments/appointment_form.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('appointments:appointment-confirmation-page')
    
    def form_valid(self, form):

        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.name = self.request.user.first_name
            form.instance.surname = self.request.user.last_name
            form.instance.email = self.request.user.email
            form.instance.phone_number = self.request.user.phone_number
        
        if form.is_valid():
            submission = form.save()

            # Send mail?

            return redirect('appointments:appointment-confirmation-page', submission_token=submission.token)

        return super().form_valid(form)
 
    
class AppointmentConfirmationView(TemplateView):
    template_name = 'appointments/appointment_confirmation.html'

    def get(self, request, submission_token):

        try:
            submitted_data = Appointment.objects.get(token=submission_token)
        except Appointment.DoesNotExist:
            raise Http404

        context = {'submitted_data': submitted_data}
        return render(request, self.template_name, context)


def available_times(request):
    json_data = json.loads(request.body)
    selected_day = json_data.get('selected_day')

    if not selected_day:
        return JsonResponse([], safe=False)
    
    available_times = Appointment.get_available_times(selected_day)
    
    return JsonResponse(available_times, safe=False)
