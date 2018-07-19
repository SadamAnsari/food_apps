from __future__ import unicode_literals, absolute_import

import logging

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from common.utils import send_templated_email
from apps.login.forms import SignUpForm, PasswordChangeCustomForm, ForgotUsernameForm
from apps.users.models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@login_required
def validate_username(request):
    logger.info("----------Request for validate username----------")
    username = request.GET['username']
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def login(request):
    template_name = "login/login.html"
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect("login:dashboard")
        else:
            return render(request, template_name, {'error_message': 'Invalid login'})
    return render(request, template_name)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            instance = form.save()
            Profile.objects.create(user=instance, first_name=instance.first_name,
                                   last_name=instance.last_name, email=instance.email)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect("user:profile")
        else:
            return render(request, 'login/signup.html', {'form': form, 'error_message': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'login/signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.is_active = False
#             instance.save()
#             Profile.objects.create(user=instance, first_name=instance.first_name,
#                                    last_name=instance.last_name, email=instance.email)
#             current_site = get_current_site(request)
#             subject = 'Activate Your {0} Account'.format("FabFood")
#             try:
#                 send_templated_email(subject=subject, email_template_name='login/account_activation_email.html',
#                                      email_context={
#                                                         'user': instance,
#                                                         'domain': current_site.domain,
#                                                         'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
#                                                         'token': account_activation_token.make_token(instance),
#                                                     },
#                                      recipients=instance.email)
#             except Exception as ex:
#                 logger.exception("Failed to sent forgot_username email.")
#                 logger.critical(
#                     "Caught exception in {}".format(__file__),
#                     exc_info=True
#                 )
#             return redirect('/account_activation_sent/')
#     else:
#         form = SignUpForm()
#     return render(request, 'login/signup.html', {'form': form, 'error_message': form.errors})


def account_activation_sent(request):
    return render(request, 'login/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        auth_login(request, user)
        return redirect('user:profile')
    else:
        return render(request, 'login/account_activation_invalid.html')



@login_required
def logout(request):
    logger.info("----------Request for user logout----------")
    try:
        auth_logout(request)
        del request.session['user_type']
    except:
        pass
    logger.info("----------User logout successfully----------")
    messages.add_message(request, messages.INFO, "You have successfully logged out.")
    return redirect("login:login")


@login_required
def dashboard(request):
    if not request.user.is_authenticated():
        return render(request, "login/login.html")
    else:
        user = request.user
        return render(request, 'login/index.html', {'user': user})


@login_required
def change_password(request):
    logger.info("----------Request for change password for user----------")
    if request.method == 'POST':
        form = PasswordChangeCustomForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            logger.info("Password changed successfully.")
            return redirect("login:dashboard")
        else:
            logger.error("Failed to change password..." + str(form.errors))
            messages.error(request, 'Please correct the error below.')
            return render(request, "login/change_password.html", {'form': form})
    else:
        form = PasswordChangeCustomForm(user=request.user)
        args = {'form': form}
        logger.info("Trying to render user change password form.")
        return render(request, "login/change_password.html", args)


def forgot_username(request):
    logger.info("----------Request for forgot username for user----------")
    if request.method == 'POST':
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            recipient = form['email'].value()
            user_instance = User.objects.filter(email__iexact=recipient)
            try:
                send_templated_email(subject='Username Detail',
                                     email_template_name='login/forgot_username_email.html',
                                     email_context={'user_name': user_instance[0].username},
                                     recipients=recipient)
                messages.add_message(request, messages.INFO,
                                     "We've emailed you username, if an account exists with the "
                                     "email you entered.")
                return HttpResponseRedirect('/forgot_username/')
            except Exception as ex:
                logger.exception("Failed to sent forgot_username email.")
                logger.critical(
                    "Caught exception in {}".format(__file__),
                    exc_info=True
                )
    else:
        form = ForgotUsernameForm()
        logger.info("Trying to render ForgotUsernameForm form.")
    return render(request, "login/forgot_username.html", {'form': form})
