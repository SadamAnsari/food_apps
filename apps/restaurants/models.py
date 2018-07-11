from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from common.base_model import Base
from .constants import ReviewStar
from common.constants import Status
from apps.users.models import Profile
from apps.masters.models import Address


class Restaurant(Base):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    street = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    cell_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.SmallIntegerField(_("Status"), choices=Status.FieldStr.items(), default=Status.Pending)
    url = models.URLField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="restaurants/images", blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "fab_restaurant"
        verbose_name = _("fab_restaurant")
        verbose_name_plural = _("fab_restaurants")
        ordering = ('name',)


class Dish(Base):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField('Rs amount', max_digits=8, decimal_places=2, blank=True, null=True)
    date = models.DateField(default=date.today)
    image = models.ImageField(upload_to="restaurants/dishes", blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.CASCADE, related_name='dishes')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "fab_dish"
        verbose_name = _("fab_dish")
        verbose_name_plural = _("fab_dishes")
        ordering = ('name',)


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(choices=ReviewStar.FieldStr.items(), default=ReviewStar.Three)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)