from django.contrib import admin

from .models import DossiersModel, DossiersAdmin

admin.site.register(DossiersModel, DossiersAdmin)
