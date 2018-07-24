from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, FoodItem, RestaurantReview, CuisineType

admin.site.register(Restaurant)
admin.site.register(CuisineType)
admin.site.register(FoodItem)
admin.site.register(RestaurantReview)
