from django.contrib import admin
from . models import userpost, BlogComment

# Register your models here.
admin.site.register((userpost, BlogComment))