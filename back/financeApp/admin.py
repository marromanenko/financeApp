from django.contrib import admin
from .models import CustomUser, Transport, Accomodation

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Transport)
admin.site.register(Accomodation)