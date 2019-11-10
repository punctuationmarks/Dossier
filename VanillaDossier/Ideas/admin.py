from django.contrib import admin

from .models import IdeasModel, ideasAdmin

admin.site.register(IdeasModel, ideasAdmin)
