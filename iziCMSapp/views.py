from django.shortcuts import render
from django.template import loader
from FTPManager import FTPManager
from FTPManager import credentials
from .forms.formUploadHtml import formUploadHtml
from django.http import HttpResponseRedirect
import logging


host = 'nexgate.ch'
user = 'j4kim'
port = 21
password = credentials.PWD
directory = 'exemple'
filename = 'index.html'

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

def websites_edit(request, website_id):
    site = Site.objects.get(id=website_id)
    template = loader.get_template('websites/edit.html')
    return HttpResponse(
        template.render({
            'site':site,
            'pages':site.page_set.all()
        }, request))

def websites_add(request):
    return HttpResponse(loader.get_template('websites/add.html').render(request))

###
### PAGES
###

def pages_edit(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)
    template = loader.get_template('pages/edit.html')
    return HttpResponse(
        template.render({'site':site,'page':page}, request))

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return HttpResponse(
        loader.get_template(
            'pages/add.html'
        ).render({'site':site},request))

###
### OTHER
###

def testFTP(request):
    # creation du ftp manager
    ftp = FTPManager.FTPManager(host,port,user,password)

    info = ""

    if request.method == 'POST':

        form = formUploadHtml(request.POST)
        if form.is_valid():
            pageContent = form.cleaned_data['pageContent']
            ftp.uploadTextInFile(directory,filename,pageContent)
            info = "Page mise à jour"

    # download
    file = ftp.downloadRead(directory,filename)

    template = loader.get_template('testFTP.html')
    context = {
        'file': file,
        'informationMessage' : info
    }
    return HttpResponse(template.render(context, request))
