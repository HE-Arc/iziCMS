from django.shortcuts import redirect, render
from django.template import loader

from FTPManager import FTPManager
import logging
from django.http import HttpResponse

from .models import Site
from bs4 import BeautifulSoup
import html

logger = logging.getLogger(__name__)

###
### HOME
###

def home(request):
    return render(request, 'home.html')

###
### WEBSITES
###

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

    return render(request, 'pages/index.html', {
            'site':site,
            'pages':site.page_set.all()
        })

def pages_edit(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.session['pwd']
    file = FTPManager.download(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path)

    # parse the file as html
    soup = BeautifulSoup(file)
    # gets the first element that match the selector
    tag = soup.select(page.selector)[0]
    # todo: handle multiple edit

    return render(request, 'pages/edit.html', {'site':site,'page':page, 'file':file, 'tag':tag.prettify()})

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return render(request, 'pages/add.html', {'site':site})

def pages_update(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.session['pwd']

    # the file content has not changed, but we need it
    file_content = request.POST['fileContent']
    # the new content of the selected element
    edit_content = request.POST['editContent']

    # parse the entire file again (todo: possible DRY?)
    file = BeautifulSoup(file_content)

    # parse the new content
    new_content = BeautifulSoup(edit_content)

    # retrieve the selected element and replace its content by the new_content
    elem = file.select(page.selector)[0]
    elem.clear()
    elem.append(new_content)

    FTPManager.upload(site.ftp_host, site.ftp_port, site.ftp_user, pwd, "", page.path, file.prettify())

    return redirect('pages_index', website_id=site.id)

###
### OTHER
###

def izi_edit(request, host, path):
    """Handle requests from the bookmarklet"""
    # todo: retrieve a Site model from host
    # todo: magic to get the page from path, try to find index.html if the path is a diretory
    # todo: redirect to pages_edit
    return HttpResponse("host: <b>{}</b>, path: <b>{}</b>".format(host, path))