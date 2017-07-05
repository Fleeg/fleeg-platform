from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',)


class LoginForm(forms.Form):
    identity = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=3, required=True)
    keep_connected = forms.BooleanField(required=False)
