from django.db import models
from django.conf import settings

class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    FTPHost = models.CharField(max_length=200, default="")
    FTPId = models.CharField(max_length=200, default="127.0.0.1")
    FTPPort = models.IntegerField(default=21)
    def __str__(self):
        return self.name

#ManyToManyField?
class UserRoleOnSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    path = models.CharField(max_length=200)
    def __str__(self):
        return self.path
