from django.contrib import admin

# Register your models here.
from .models import Site
from .models import UserRoleOnSite

admin.site.register(Site)
admin.site.register(UserRoleOnSite)
