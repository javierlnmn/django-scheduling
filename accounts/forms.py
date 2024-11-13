from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

CustomUserModel = get_user_model()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=255, required=True)
    old_password = forms.CharField(max_length=255, required=False)
    new_password = forms.CharField(max_length=255, required=False)
    confirm_password = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'phone_number', 'email')
        exclude = ('password',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        user = self.request.user

        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password:
            if not user.check_password(old_password):
                self.add_error("old_password", "The old password is incorrect.")
            if new_password != confirm_password:
                self.add_error("confirm_password", "New passwords do not match.")
            try:
                password_validation.validate_password(new_password, self.instance)
            except ValidationError as e:
                self.add_error("new_password", e)

        return cleaned_data