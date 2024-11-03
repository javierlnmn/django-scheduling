from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'display_profile_picture')
    search_fields = ('username', 'email')

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            display = format_html(f'<img src="{obj.profile_picture.url}" alt="User\'s profile picture" style="width: 50px; height: auto; aspect-ratio: 1; object-fit: cover;"')
        else:
            display = format_html('<span>No profile picture</span>')
        return display