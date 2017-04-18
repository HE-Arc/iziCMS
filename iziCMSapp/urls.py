from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^connect_hostname$', views.connect_hostname, name='connect_hostname'),
    url(r'^disconnect$', views.disconnect, name='disconnect'),

    url(r'^websites/connect$', views.websites_connect, name='websites_connect'),

    url(r'^websites/(?P<website_id>[0-9]+)/configure', views.websites_configure, name='websites_configure'),
    url(r'^websites/(?P<website_id>[0-9]+)/delete', views.websites_delete, name='websites_delete'),

    url(r'^websites/(?P<website_id>[0-9]+)/pages/$', views.pages_index, name='pages_index'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/add$', views.pages_add, name='pages_add'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/update_config$', views.pages_update_config, name='pages_update_config'),

    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)$', views.pages_edit, name='pages_edit'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)/update$', views.pages_update, name='pages_update'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)/configure$', views.pages_configure, name='pages_configure'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)/delete', views.pages_delete, name='pages_delete'),

    url(r'^izi_edit/(?P<hostname>(\w|\.)+)/(?P<path>.+)$', views.izi_edit, name='izi_edit'), # (\w|\.)+ lettres ou .
]
