from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # need to add honeypots

    path('admin/', admin.site.urls),
    path('', include('Main_Templates.urls')),
    path('workIdeas/', include('WorkIdeas.urls')),
    path('dossiers/', include('Dossiers.urls')),
    path('thoughts/', include('Thoughts.urls'))
]
