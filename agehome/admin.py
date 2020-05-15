from django.contrib import admin
from agehome.models import SigningUser, ContactUser, Profile

# Register your models here.
admin.site.register((SigningUser, ContactUser, Profile))