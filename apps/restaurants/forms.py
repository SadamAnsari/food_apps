from django import forms

from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=255, required=False)
    telephone = forms.CharField(max_length=20, required=False)
    cell_phone = forms.CharField(max_length=20, required=False)
    url = forms.URLField(max_length=255, required=False)
    image = forms.ImageField(required=False)
    street = forms.Textarea()

    class Meta:
        model = Restaurant
        fields = ('name', 'email', 'telephone', 'cell_phone', 'url', 'image')
