from django.shortcuts import redirect, render

from FTPManager import FTPManager
import logging
import http.client
from django.contrib import messages
import http.client

from .models import Site, Page
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def testHTTP(hostname):
    try:
        c = http.client.HTTPConnection(hostname)
        c.request("HEAD", '')
        return True
    except:
        return False

###
### HOME
###

def home(request):
    """
    Show a simple form asking for a website hostname and a password.
    The form is sent to the connect_hostname view method.
    """
    if 'site' in request.session:
        messages.info(request, 'You are connected, click your hostname in the header to disconnect')
        return redirect('pages_index', website_id=request.session['site'])
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
            # everything's good
            request.session['site'] = site.id
            request.session['pwd'] = pwd
            return redirect('pages_index', website_id=site.id)
        else:
            messages.error(request, "Unable to connect to your FTP server, please verify your configuration.")
            return redirect('websites_configure', site.id)
    except Site.DoesNotExist:
        messages.warning(request, "We don't know your website yet, please register it using your FTP crendentials.")
        return render(request, 'websites/configure.html', {
                'site':{'hostname':hostname},
                'pwd':pwd
            })

def disconnect(request):
    request.session.clear()
    messages.info(request, 'You are disconnected')
    return redirect('home')

###
### WEBSITES
###

def websites_create(request):
    """
    Create a website using the POST parameters.
    Store hostname and password in the user session and open the page index of the site.
    """
    hostname = request.POST['hostname']
    ftp_host = request.POST['ftp_host']
    ftp_port = request.POST['ftp_port']
    root_folder = request.POST['root_folder']
    ftp_user = request.POST['ftp_user']
    pwd = request.POST['pwd']

    if not FTPManager.test(ftp_host, ftp_port, ftp_user, pwd, root_folder) or not testHTTP(hostname):
        messages.warning(request, "Unable to connect to your FTP server, please verify your configuration.")
        return render(request, 'websites/configure.html', {
            'site': request.POST.dict(), 'pwd':pwd
        })

    site = Site.objects.create(
        hostname=hostname, ftp_host=ftp_host, ftp_port=ftp_port,
        root_folder=root_folder, ftp_user=ftp_user
    )

    request.session['site'] = site.id
    request.session['pwd'] = pwd

    messages.success(request, 'Website successfully created')
    return redirect('pages_index', website_id=site.id)


def websites_update(request, website_id):
    """
    Update a website using the POST parameters.
    Store hostname and password in the user session and open the page index of the site.
    """
    site = Site.objects.filter(id=website_id)

    hostname = request.POST['hostname']
    ftp_host = request.POST['ftp_host']
    ftp_port = request.POST['ftp_port']
    root_folder = request.POST['root_folder']
    ftp_user = request.POST['ftp_user']
    pwd = request.POST['pwd']

    if not FTPManager.test(ftp_host, ftp_port, ftp_user, pwd) or not testHTTP(hostname):
        messages.warning(request, "Unable to connect to your FTP server, please verify your configuration.")
        return redirect('websites_configure', website_id=site.get().id)

    site.update(
        hostname=hostname, ftp_host=ftp_host,
        ftp_user=ftp_user, ftp_port=ftp_port,
        root_folder=root_folder
    )

    request.session['site'] = site.get().id
    request.session['pwd'] = pwd

    messages.success(request, 'Website successfully updated')
    return redirect('pages_index', website_id=site.get().id)

def websites_configure(request, website_id):
    """
    Show the form to configure an existing or new website.
    """
    site = Site.objects.get(id=website_id)
    return render(request, 'websites/configure.html', {
        'site': site
    })

def websites_delete(request, website_id):
    Site.objects.get(id=website_id).delete()
    messages.success(request, 'Website successfully deleted')
    return redirect('disconnect')

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

    file = FTPManager.download(site.ftp_host, site.ftp_port, site.ftp_user, pwd, site.root_folder, page.path)

    if file:
        # parse the file as html
        soup = BeautifulSoup(file, "html.parser")

        # gets all elements that match the selector
        tags = soup.select(page.selector)
        if len(tags) > 0:
            listEditableContent = [tag.decode_contents(formatter="html") for tag in tags]
            return render(request, 'pages/edit.html',
                          {'site': site, 'page': page, 'file': file, 'listEditableContent': listEditableContent})

        messages.warning(request, 'Selector {} not found on the page'.format(page.selector))

    else:
        messages.error(request, 'Page not found, please check the path of the page')

    return render(request, 'pages/configure.html', {'site':site, 'page':page})

def pages_update(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)

    pwd = request.session['pwd']

    # the file content has not changed, but we need it
    file_content = request.POST['fileContent']

    # parse the entire file again (todo: possible DRY?)
    file = BeautifulSoup(file_content, "html.parser")

    # update all editable contents
    tags = file.select(page.selector)
    for i,content in enumerate(request.POST.getlist('editContent')):
        # the new content of the selected element
        print("editContent " + content)
        # parse the new content
        new_content = BeautifulSoup(content, "html.parser")

        # retrieve the selected element and replace its content by the new_content
        elem = tags[i]
        elem.clear()
        elem.append(new_content)

    # upload the file
    FTPManager.upload(site.ftp_host, site.ftp_port, site.ftp_user, pwd, site.root_folder, page.path, file.prettify())

    messages.success(request, 'Page successfully edited !')
    return redirect('pages_index', website_id=site.id)

def pages_add(request, website_id):
    site = Site.objects.get(id=website_id)
    return render(request, 'pages/configure.html', {'site':site, 'is_new':True})

def pages_configure(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)
    return render(request, 'pages/configure.html', {'site':site, 'page':page, 'is_new':False})

def pages_add_config(request, website_id):
    site = Site.objects.get(id=website_id)
    path = request.POST['path']
    selector = request.POST['selector']

    page = Page.objects.create(
        site=site, path=path, selector=selector
    )
    messages.success(request, "Page successfully added")
    return redirect('pages_index', website_id=site.id)

def pages_update_config(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.filter(id=page_id)
    path = request.POST['path']
    selector = request.POST['selector']

    page.update(
        site=site, path=path, selector=selector
    )
    return redirect('pages_index', website_id=site.id)

def pages_delete(request, website_id, page_id):
    site = Site.objects.get(id=website_id)
    page = site.page_set.get(id=page_id)
    page.delete()
    messages.success(request, 'Page successfully deleted !')
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
        messages.info(request, "We don't know your website. You can create a new configuration here.")
        return render(request, 'websites/configure.html', {
            'site':{'hostname': hostname}, 'is_new':True
        })


    # try to find index.html if the path is a diretory
    if path.endswith('/'):
        path += 'index.html'
    try:
        page = site.page_set.get(path=path)
    except Page.DoesNotExist:
        # if it fails, propose to add the page
        messages.info(request, "This page is not configured yet.")
        return render(request, 'pages/configure.html', {
            'site':site,
            'is_new':True,
            'page':{'path':path}})

    return redirect('pages_edit', website_id=site.id, page_id=page.id)
