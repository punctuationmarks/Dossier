from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # need to add honeypots

    path('admin/', admin.site.urls),
    path('', include('Main_Templates.urls')),
    path('dossiers/', include('Dossiers.urls')),
    path('ideas/', include('Ideas.urls')),
    path('thoughts/', include('Thoughts.urls'))
]
