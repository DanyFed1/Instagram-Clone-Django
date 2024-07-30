from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.contrib.auth.models import User

class MyAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account already exists with this email address.")
        return email

    def clean_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("The username is invalid.")
        return username
