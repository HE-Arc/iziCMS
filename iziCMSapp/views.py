from django.shortcuts import redirect, render

from FTPManager import FTPManager
import logging

from .models import Site, Page
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

###
### HOME
###

def home(request):
    """
    Show a simple form asking for a website hostname and a password.
    The form is sent to the connect_hostname view method.
    """
    return render(request, 'home.html')

def connect_hostname(request):
    """
    If the hostname is known, perform a FTP test, store hostname
    and password in session and redirect to pages_index
    Else, show websites_configure view.
    """
    hostname = request.POST['hostname']
    pwd = request.POST['pwd']

    try:
        site = Site.objects.get(hostname=hostname) # exception raised here if the site is unknown
        if FTPManager.test(site.ftp_host, site.ftp_port, site.ftp_user, pwd):
            request.session['hostname'] = hostname
            request.session['pwd'] = pwd
            return redirect('pages_index', website_id=site.id)
        else:
            return render(request, 'websites/configure.html', {
                'hostname': hostname,
                'ftp_host': site.ftp_host,
                'port': site.ftp_host,
                'username': site.ftp_user,
                'pwd': pwd,
                'is_new': False,
                'message': "Unable to connect to your FTP server, please verify your configuration."
            })
    except Site.DoesNotExist:
        return render(request, 'websites/configure.html', {
                'hostname':hostname,
                'pwd':pwd,
                'is_new':True,
                'message':"We don't know your website yet, please register it using your FTP crendentials."
            })


###
### WEBSITES
###

def websites_connect(request):
    """
    Create or update a website using the POST parameters.
    The is_new hidden input in websites_configure tells what to do.
    Store hostname and password in the user session and open the page index of the site.
    """
    hostname = request.POST['hostname']
    ftp_host = request.POST['ftp_host']
    port = request.POST['port']
    username = request.POST['username']
    pwd = request.POST['pwd']
    is_new = request.POST['is_new']

    if not FTPManager.test(ftp_host, port, username, pwd):
        return render(request, 'websites/configure.html', {
            'hostname': hostname,
            'ftp_host': ftp_host,
            'port': port,
            'username': username,
            'pwd': pwd,
            'message': "Unable to connect to your FTP server, please verify your configuration."
        })

    # in fact the flag is_new may be useless
    site, created = Site.objects.update_or_create(
        hostname=hostname, ftp_host=ftp_host,
        ftp_user=username, ftp_port=port
    )

    request.session['hostname'] = hostname
    request.session['pwd'] = pwd

    return redirect('pages_index', website_id=site.id)


def websites_configure(request, website_id):
    """
    Show the form to configure an existing or new website.
    """
    #todo

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

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return render(request, 'pages/configure.html', {'site':site})

def pages_update_config(request, website_id):
    site = Site.objects.get(id=website_id)
    path = request.POST['path']
    selector = request.POST['selector']
    page, created = Page.objects.update_or_create(
        site=site, path=path, selector=selector
    )
    return redirect('pages_index', website_id=site.id)

###
### OTHER
###

def izi_edit(request, hostname, path):
    """Handle requests from the bookmarklet"""
    # Retrieve a Site model from hostname
    try:
        site = Site.objects.get(hostname=hostname)
    except Site.DoesNotExist:
        return render(request, 'websites/configure.html', {
            'hostname': hostname,
            'message': "We don't know your website. You can create a new configuration here."
        })

    try:
        page = site.page_set.get(path=path)
    except Page.DoesNotExist:
        # todo: magic to get the page from path, try to find index.html if the path is a diretory
        # if it fails, propose to add the page
        return render(request, 'pages/configure.html', {
            'site':site,
            'path':path,
            'message':"This page is not configured yet."})

    return redirect('pages_edit', website_id=site.id, page_id=page.id)