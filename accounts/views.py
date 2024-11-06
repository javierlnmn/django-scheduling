from django.views.generic.edit import FormView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect

class UserRegistrationFormView(FormView):
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('common:index')
    
    def form_valid(self, form):

        if form.is_valid():
            form.save()
            return redirect('common:index')

        return super().form_valid(form)