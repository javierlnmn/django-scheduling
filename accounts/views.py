from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from appointments.models import Appointment
from .models import CustomUser
from .forms import UserRegistrationForm, UserProfileForm

class UserRegistrationFormView(FormView):
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('common:index')
    
    def form_valid(self, form):

        if form.is_valid():
            user = form.save()

            user_email = form.instance.email

            user_appointments = Appointment.objects.filter(email=user_email)
            user_appointments.update(
                user=user,
                name=user.name,
                surname=user.surname,
            )

            self.request.user = user

            return redirect('common:index')

        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        new_password = form.cleaned_data.get('new_password')
        if new_password:
            self.object.set_password(new_password)
            update_session_auth_hash(self.request, self.object)
            messages.success(self.request, 'Password updated.')


        self.object = form.save()
        messages.success(self.request, 'Profile details updated.')

        return super().form_valid(form)