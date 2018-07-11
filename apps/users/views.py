from __future__ import unicode_literals, absolute_import
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from apps.users.models import Profile
from apps.masters.models import State
from .forms import EditProfileForm, EditAddressForm
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


@login_required
def user_profile(request):
    logger.info("----- GET Request for User Profile ----- ")
    template_name = 'users/user_profile.html'
    profile = get_object_or_404(Profile, user_id=request.user.id)
    state = State.objects.all().order_by('name')
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST or None)
        address_form = EditAddressForm(request.POST or None)
        for item in [profile_form, address_form]:
            if not item.is_valid():
                data = {'profile': profile, 'states': state, 'error_message': item.errors}
                return render(request, template_name, data)
        if request.POST and profile_form.is_valid() and address_form.is_valid():
            profile_form.save(commit=False)
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.email = request.POST.get('email')
            profile.cell_phone = request.POST.get('cell_phone')
            address_instance = address_form.save()
            profile.address = address_instance
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect("user:profile")
    else:
        profile_form = EditProfileForm()
    return render(request, template_name, {'form': profile_form, 'profile': profile, 'states': state})


