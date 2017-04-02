from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^websites/connect$', views.websites_connect, name='websites_connect'),

    url(r'^websites/(?P<website_id>[0-9]+)/pages/$', views.pages_index, name='pages_index'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)$', views.pages_edit, name='pages_edit'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/add$', views.pages_add, name='pages_add'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)/update$', views.pages_update, name='pages_update'),
]
