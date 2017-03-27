from django.db import models
from django.conf import settings

class Site(models.Model):
    name = models.CharField(max_length=200, default="")
    ftp_host = models.CharField(max_length=200, default="")
    ftp_user = models.CharField(max_length=200, default="")
    ftp_port = models.IntegerField(default=21)
    url = models.URLField(default="")

    class Meta:
        unique_together = ('ftp_host', 'ftp_user')

    def __str__(self):
        return self.name

class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    path = models.CharField(max_length=200, default="")
    selector = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.path
