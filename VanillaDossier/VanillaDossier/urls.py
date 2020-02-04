from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

# for handling static files on development server locally
# but testing debug === False
 

from django.conf.urls.static import static
urlpatterns = [
    # need to add honeypots

    path('admin/', admin.site.urls),
    path('', include('Main_Templates.urls')),
    path('dossiers/', include('Dossiers.urls')),
    path('ideas/', include('Ideas.urls')),
    path('thoughts/', include('Thoughts.urls'))
]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
