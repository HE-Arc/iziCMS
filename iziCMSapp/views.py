from django.shortcuts import redirect
from django.template import loader
from FTPManager import FTPManager
import logging

from django.http import HttpResponse
from .models import Site

logger = logging.getLogger(__name__)

###
### HOME
###

def home(request):
    return HttpResponse(loader.get_template('home.html').render(request))

###
### WEBSITES
###

def websites_index(request):
    sites = Site.objects.all()
    template = loader.get_template('websites/index.html')
    context = {
        'sites': sites,
    }
    return HttpResponse(template.render(context, request))

def websites_add(request):
    return HttpResponse(loader.get_template('websites/add.html').render(request))

###
### PAGES
###

def pages_index(request, website_id):
    site = Site.objects.get(id=website_id)
    template = loader.get_template('pages/index.html')
    return HttpResponse(
        template.render({
            'site':site,
            'pages':site.page_set.all()
        }, request))

def pages_edit(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.POST['password']
    ftp = FTPManager.FTPManager(site.ftp_host, site.ftp_port, site.ftp_user, pwd)
    file = ftp.downloadRead("", page.path)

    template = loader.get_template('pages/edit.html')

    return HttpResponse(
        template.render({'site':site,'page':page, 'file':file}, request))

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return HttpResponse(
        loader.get_template(
            'pages/add.html'
        ).render({'site':site},request))

def pages_update(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.POST['password']
    pageContent = request.POST['pageContent']

    ftp = FTPManager.FTPManager(site.ftp_host, site.ftp_port, site.ftp_user, pwd)
    ftp.uploadTextInFile("", page.path, pageContent)

    return redirect('pages_index', website_id=site.id)

###
### OTHER
###