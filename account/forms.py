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
    keep_connected = forms.BooleanField(initial=False, required=False)


class SettingsForm(forms.Form):
    first_name = forms.CharField(min_length=3, required=True)
    last_name = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=3, required=False)
    confirm_password = forms.CharField(min_length=3, required=False)

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError('Password confirmation does not equal with password.',)
        return password
