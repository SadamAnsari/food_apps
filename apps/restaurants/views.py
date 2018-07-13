import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RestaurantForm
from apps.masters.models import State
from apps.users.forms import EditAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.users.models import Profile
from apps.restaurants.models import CuisineType, Restaurant, RestaurantCuisine

logger = logging.getLevelName(__file__)


@login_required
def add_restaurants(request):
    state = State.objects.all().order_by('name')
    current_user = Profile.objects.get(user__id=request.user.id)
    cuisine_types = CuisineType.objects.order_by('name')
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST or None, request.FILES or None)
        address_form = EditAddressForm(request.POST or None)
        if request.POST and restaurant_form.is_valid() and address_form.is_valid():
            res_instance = restaurant_form.save(commit=False)
            res_instance.user = current_user
            address_instance = address_form.save()
            res_instance.address = address_instance
            res_instance.save()
            if restaurant_form.cleaned_data['cuisine']:
                for c_type in restaurant_form.cleaned_data['cuisine']:
                    instance = RestaurantCuisine.objects.create(restaurant=res_instance, cuisine_type=c_type)
                    instance.save()
            messages.success(request, 'Restaurant added successfully.')
            return redirect("restaurant:view_restaurant")
    else:
        restaurant_form = RestaurantForm()
    data = {'form': restaurant_form, 'states': state, "types": cuisine_types}
    return render(request, template_name="restaurants/restaurant_registration.html", context=data)


@login_required
def view_restaurants(request):
    profile = Profile.objects.get(user__id=request.user.id)
    restaurants = Restaurant.objects.filter(user__id=profile.id)
    c_type_dict = {}
    for restaurant in restaurants:
        cuisine_types = RestaurantCuisine.objects.filter(restaurant_id=restaurant.id)
        c_type_dict[restaurant.id] = []
        if cuisine_types:
            for c_type in cuisine_types:
                obj = CuisineType.objects.get(pk=c_type.cuisine_type_id)
                c_type_dict[restaurant.id].append(obj.name)
    data = {"restaurants": restaurants, "c_type": c_type_dict}
    return render(request, template_name="restaurants/view_restaurants.html", context=data)


@login_required
def update_restaurant(request, id):
    state = State.objects.all().order_by('name')
    current_user = Profile.objects.get(user__id=request.user.id)
    restaurant = get_object_or_404(Restaurant, pk=id)
    cuisine_types = CuisineType.objects.order_by('name')
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST or None, request.FILES or None, instance=restaurant)
        address_form = EditAddressForm(request.POST or None, instance=restaurant.address)
        if request.POST and restaurant_form.is_valid() and address_form.is_valid():
            res_instance = restaurant_form.save(commit=False)
            res_instance.user = current_user
            address_instance = address_form.save()
            res_instance.address = address_instance
            res_instance.save()
            messages.success(request, 'Restaurant updated successfully.')
            return redirect("restaurant:view_restaurant")
    else:
        restaurant_form = RestaurantForm()
        data = {"form": restaurant_form,
                "profile": restaurant,
                "states": state,
                "types": cuisine_types
                }
        return render(request, template_name="restaurants/update_restaurant.html", context=data)


@login_required
def delete_restaurant(request, id):
    profile = Profile.objects.get(user__id=request.user.id)
    restaurant = Restaurant.objects.get(pk=id)
    restaurant.delete()
    messages.success(request, 'Restaurant(%s) deleted successfully.' % restaurant.name)
    restaurants = Restaurant.objects.filter(user__id=profile.id)
    data = {"restaurants": restaurants}
    return render(request, template_name="restaurants/view_restaurants.html", context=data)

