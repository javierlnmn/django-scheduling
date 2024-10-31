import secrets
from django.utils import timezone

def generate_unique_token(length=32):
    token = secrets.token_urlsafe(length)
    return token