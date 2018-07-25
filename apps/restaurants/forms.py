from django import forms
from .constants import Course
from .models import Restaurant, CuisineType, FoodItem


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=255, required=False)
    telephone = forms.CharField(max_length=20, required=False)
    cell_phone = forms.CharField(max_length=20, required=False)
    url = forms.URLField(max_length=255, required=False, initial="http://")
    image = forms.ImageField(required=False)
    street = forms.CharField(max_length=200, required=False)
    cuisine = forms.ModelMultipleChoiceField(queryset=CuisineType.objects.all(),
                                             widget=forms.CheckboxSelectMultiple(),
                                             required=False)

    class Meta:
        model = Restaurant
        fields = ('name', 'email', 'telephone', 'cell_phone', 'url', 'image', 'street','cuisine')


class FoodItemForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True)
    description = forms.Textarea()
    price = forms.CharField(max_length=10, required=True)
    image = forms.ImageField(required=False)
    cuisine = forms.ModelChoiceField(queryset=CuisineType.objects.all())
    restaurant = forms.ModelChoiceField(queryset=Restaurant.objects.all())
    course = forms.IntegerField(required=False)

    class Meta:
        model = FoodItem
        exclude = ('order_count', )
        fields = ('name', 'description', 'price', 'image', 'cuisine', 'restaurant', 'course')