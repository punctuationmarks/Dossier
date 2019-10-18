from django.contrib import admin

from .models import WorkIdeasModel, WorkIdeasAdmin

admin.site.register(WorkIdeasModel, WorkIdeasAdmin)
