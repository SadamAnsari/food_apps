from __future__ import unicode_literals, absolute_import
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from apps.masters.models import State
from apps.users.forms import EditAddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.users.models import Profile
from apps.restaurants.models import CuisineType, Restaurant, RestaurantCuisine, FoodItem

logger = logging.getLevelName(__file__)


@login_required
def add_order(request):
    profile = Profile.objects.get(user__id=request.user.id)
    restaurants = Restaurant.objects.filter(user__id=profile.id)
    data = {}
    for res in restaurants:
        food_items = FoodItem.objects.filter(restaurant__id=res.id)
        data[res] = food_items
    result = {"data": data}
    return render(request, template_name="orders/add_order.html", context=result)


@login_required
def add_cart(request):
    return HttpResponse("You are at add to cart page")



