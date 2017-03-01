from django.db import models
from django.conf import settings

class Site(models.Model):
    name = models.CharField(max_length=200, default="")
    url = models.CharField(max_length=200, default="")
    FTPHost = models.CharField(max_length=200, default="")
    FTPId = models.CharField(max_length=200, default="127.0.0.1")
    FTPPort = models.IntegerField(default=21)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    def __str__(self):
        return self.name

class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    path = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, default="")
    selector = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.path
