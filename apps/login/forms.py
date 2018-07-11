from __future__ import unicode_literals, absolute_import

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 max_length=30, required=False, label='First Name', label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                max_length=30, required=False, label='Last Name', label_suffix="")
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             max_length=254, required=True, label='Email', label_suffix="")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30, required=True, label='Username', label_suffix="")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                max_length=50, required=True, label='Password', label_suffix="")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                max_length=50, required=True, label='Confirm Password', label_suffix="")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email is already taken.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Old Password not matching')
        return old_password


class ForgotUsernameForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email