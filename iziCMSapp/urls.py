from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.websites_index, name='websites_index'),
    url(r'^websites/(?P<website_id>[0-9]+)$', views.websites_edit, name='websites_edit'),
    url(r'^websites/add$', views.websites_add, name='websites_add'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/(?P<page_id>[0-9]+)$', views.pages_edit, name='pages_edit'),
    url(r'^websites/(?P<website_id>[0-9]+)/pages/add$', views.pages_add, name='pages_add'),
    url(r'^testFTP/', views.testFTP, name='testFTP'),
]
