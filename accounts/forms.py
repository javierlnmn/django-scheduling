from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUserModel = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'email', 'password1', 'password2')