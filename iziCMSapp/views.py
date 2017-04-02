from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, csrf_exempt

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

@csrf_exempt # sans ça erreur csrf impossible à résoudre
def websites_connect(request):
    host = request.POST['host']
    port = request.POST['port']
    username = request.POST['username']
    pwd = request.POST['pwd']

    # todo: ftp test, redirect back if it fails

    try:
        site = Site.objects.get(ftp_host=host, ftp_user=username)
    except Site.DoesNotExist:
        return redirect('home')
        # todo: create a website

    request.session['pwd'] = pwd

    return redirect('pages_index', website_id=site.id)

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

    pwd = request.session['pwd']
    file = FTPManager.download(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path)

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

    pwd = request.session['pwd']
    pageContent = request.POST['pageContent']

    FTPManager.upload(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path, pageContent)

    return redirect('pages_index', website_id=site.id)

###
### OTHER
###
