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

def websites_index(request):
    sites = Site.objects.all()
    template = loader.get_template('iziCMS/websites.index.html')
    context = {
        'sites': sites,
    }
    return HttpResponse(template.render(context, request))

def websites_edit(request, website_id=0):
    site = Site.objects.get(id=website_id)
    template = loader.get_template('iziCMS/websites.edit.html')
    return HttpResponse(template.render({'site':site}, request))

def testFTP(request):
    # creation du ftp manager
    ftp = FTPManager.FTPManager(host,port,user,password)

    # download
    file = ftp.downloadRead(directory,filename)

    template = loader.get_template('iziCMS/testFTP.html')
    context = {
        'file': file,
    }
    return HttpResponse(template.render(context, request))

def submitFTP(request):

    if request.method == 'POST':

        form = formUploadHtml(request.POST)
        if form.is_valid():
            # creation du ftp manager
            ftp = FTPManager.FTPManager(host,port,user,password)
            pageContent = form.cleaned_data['pageContent']
            ftp.uploadTextInFile(directory,filename,pageContent)
            return HttpResponseRedirect('/')

        # creation du ftp manager
    ftp = FTPManager.FTPManager(host,port,user,password)

        # download
    file = ftp.downloadRead(directory,filename)

    template = loader.get_template('iziCMS/testFTP.html')
    context = {
        'file': file,
    }
    return HttpResponse(template.render(context, request))
