from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    # need to add honeypots

    path('admin/', admin.site.urls),
    path('', include('Main_Templates.urls')),
    path('dossiers/', include('Dossiers.urls')),
    path('ideas/', include('Ideas.urls')),
    path('thoughts/', include('Thoughts.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

]
