from django.db import models
from django.conf import settings

# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class UserRoleOnSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    isAdmin = models.BooleanField()
