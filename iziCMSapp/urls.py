from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.websites_index, name='websites_index'),
    url(r'^websites/(?P<website_id>[0-9]+)$', views.websites_edit, name='websites_edit'),
    url(r'^testFTP/', views.testFTP, name='testFTP'),
    url(r'^submitFTP/', views.testFTP, name='submitFTP'),
]
