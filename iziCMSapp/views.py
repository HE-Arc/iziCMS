from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .models import Site, UserRoleOnSite


def index(request):
    sites = Site.objects.all()
    template = loader.get_template('iziCMS/index.html')
    context = {
        'sites': sites,
    }
    return HttpResponse(template.render(context, request))
