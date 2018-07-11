import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RestaurantForm
from apps.masters.models import State
from apps.users.forms import EditAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.users.models import Profile

logger = logging.getLevelName(__file__)


@login_required
def add_restaurants(request):
    state = State.objects.all().order_by('name')
    current_user = Profile.objects.get(user__id=request.user.id)
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST or None, request.FILES or None)
        address_form = EditAddressForm(request.POST or None)
        if request.POST and restaurant_form.is_valid() and address_form.is_valid():
            res_instance = restaurant_form.save(commit=False)
            res_instance.user = current_user
            address_instance = address_form.save()
            res_instance.address = address_instance
            res_instance.save()
            messages.success(request, 'Restaurant added/updated successfully.')
            return redirect("restaurant:view_restaurant")
    else:
        restaurant_form = RestaurantForm()
    data = {'form': restaurant_form, 'states': state}
    return render(request, template_name="restaurants/restaurant_registration.html", context=data)

@login_required
def view_restaurants(request):
    return HttpResponse("Welcome to View Restaurants Page")
