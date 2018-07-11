from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, Dish, RestaurantReview

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(RestaurantReview)
