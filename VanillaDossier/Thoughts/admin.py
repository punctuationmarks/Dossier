from django.contrib import admin

from .models import ThoughtsModel, ThoughtsAdmin

admin.site.register(ThoughtsModel, ThoughtsAdmin)
