from __future__ import unicode_literals, absolute_import

from django.db import models
from common.base_model import Base


class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3, unique=True)
    short_name = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "masters_state"

    def __unicode__(self):
        return self.name


class Address(Base):
    address = models.TextField(default='', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State, null=True)

    class Meta:
        db_table = "masters_address"

    def __unicode__(self):
        return self.address