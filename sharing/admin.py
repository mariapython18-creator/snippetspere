

from django.contrib import admin

from .models import CustomUser, DeveloperProfile,Snippet

admin.site.register(CustomUser)

admin.site.register(Snippet)

admin.site.register(DeveloperProfile)

# Register your models here.
