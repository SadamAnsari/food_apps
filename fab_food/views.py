from __future__ import unicode_literals, absolute_import
from django.shortcuts import render


def page_not_found(request):
    return render(request, "fab_food/404.html")


def internal_server_error(request):
    return render(request, "fab_food/500.html")