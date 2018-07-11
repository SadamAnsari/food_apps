from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from common.constants import Status
from common.base_model import Base
from apps.masters.models import Address


class Profile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=100, null=True, blank=True)
    profile_image = models.ImageField(_("Profile Image"), upload_to='profile/user', null=True, blank=True)
    status = models.SmallIntegerField(_("Status"), choices=Status.FieldStr.items(), default=Status.Approved)
    cell_phone = models.CharField(_("Mobile Number"), max_length=15, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "fab_user"
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __unicode__(self):
        return self.first_name
