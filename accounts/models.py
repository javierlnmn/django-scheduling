from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    @property
    def profile_picture_url(self):
        print(static('images/default_user_avatar.png'))
        return self.profile_picture.url if self.profile_picture else static('images/default_user_avatar.png')

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'