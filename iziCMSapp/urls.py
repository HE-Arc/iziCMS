from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testFTP/', views.testFTP, name='testFTP'),
    url(r'^submitFTP/', views.testFTP, name='submitFTP'),
]
