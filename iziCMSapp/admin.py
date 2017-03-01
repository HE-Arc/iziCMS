from django.contrib import admin

# Register your models here.
from .models import Site
from .models import Page

admin.site.register(Site)
admin.site.register(Page)
