import re
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',)
        User._meta.get_field('email')._unique = True
        User._meta.get_field('email').blank = False
        User._meta.get_field('email').null = False
        User._meta.get_field('first_name').blank = False
        User._meta.get_field('first_name').null = False
        User._meta.get_field('last_name').blank = False
        User._meta.get_field('last_name').null = False

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[A-Za-z0-9]+$', username):
            raise forms.ValidationError('Username does not allow special characters.')
        return username.lower()

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


class LoginForm(forms.Form):
    identity = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=3, required=True)
    keep_connected = forms.BooleanField(required=False)
