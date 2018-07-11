from __future__ import unicode_literals, absolute_import
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.masters.models import Address, State
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=False, help_text='Inform a valid email address.')
    profile_image = forms.ImageField(required=False)
    cell_phone = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'profile_image', 'cell_phone')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("User registered with the specified email address!!")
        else:
            return email


class EditAddressForm(forms.ModelForm):
    address = forms.Textarea()
    city = forms.CharField(max_length=100, required=False, help_text='Optional.')
    zip = forms.CharField(max_length=10, required=False, help_text='Optional.')
    state = forms.ModelChoiceField(queryset=State.objects.all(), required=False)

    class Meta:
        model = Address
        fields = ('address', 'city', 'zip', 'state')