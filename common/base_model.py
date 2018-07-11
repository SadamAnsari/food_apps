from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _

from django.db import models


class Base(models.Model):
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True)
    updated_date = models.DateTimeField(
        _("Last Updated Date"), auto_now=True)

    class Meta:
        abstract = True
