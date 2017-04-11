from django.db import models
from django.conf import settings

class Site(models.Model):
    # the "http" host of the website: www.exemple.com
    hostname = models.CharField(max_length=255, default="", unique=True)
    # the ftp host can be the same as well as totally different, common case: ftp.exemple.com
    ftp_host = models.CharField(max_length=255, default="")
    ftp_user = models.CharField(max_length=255, default="")
    ftp_port = models.IntegerField(default=21) # 21 in most cases

    # the base folder of the site in the ftp arborescence, not always /
    root_folder = models.CharField(max_length=255, default="/")

    def __str__(self):
        return self.hostname

class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, default="")
    selector = models.CharField(max_length=255, default="body")

    def __str__(self):
        return self.path
