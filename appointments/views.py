from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.conf import settings

from appointments.forms import CitaForm
from appointments.models import Cita

import json

# class CitaFormView(FormView):
#     template_name = 'pages/appointments/appointment-form.html'
#     form_class = CitaForm
#     success_url = reverse_lazy('appointments:appointment_confirmation_page')
    
#     def form_valid(self, form):
        
#         if form.is_valid():
#             submission = form.save()

#             html_template = get_template('pages/appointments/appointment-email.html')
#             html_content = html_template.render({ 'submission': submission })
            
#             subject = 'Cita en centro médico Psicomadrid'
#             message = f'Su cita del día {submission.fecha_cita} a las {submission.hora_cita} ha sido confirmada.'
            
#             try:

#                 send_mail(
#                     subject,
#                     message,
#                     settings.EMAIL_HOST_USER,
#                     [submission.email],
#                     html_message=html_content,
#                 )
            
#             except:
#                 # In case the email isn't send, we will just redirect to the confirmation page as usual
#                 pass

#             return redirect('appointments:appointment_confirmation_page', submission_token=submission.token_validez)

#         return super().form_valid(form)
 
    
# class CitaConfirmationView(TemplateView):
#     template_name = 'pages/appointments/appointment-confirmation.html'

#     def get(self, request, submission_token):

#         submitted_data = Cita.objects.get(token_validez=submission_token)

#         context = {'submitted_data': submitted_data}
#         return render(request, self.template_name, context)

# def horas_disponibles(request):
#     json_data = json.loads(request.body)
#     selected_day = json_data.get('selected_day')
    
#     available_hours = Cita.get_available_times(selected_day)
    
#     return JsonResponse(available_hours, safe=False)
