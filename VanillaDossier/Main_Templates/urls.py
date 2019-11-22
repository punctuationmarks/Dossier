from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('dossiers/upload-csv/', views.upload_csv_dossier, name='upload_csv_dossier'),
    path('thoughts/upload-csv/', views.upload_csv_thoughts, name='upload_csv_thoughts'),
    path('ideas/upload-csv/', views.upload_csv_ideas, name='upload_csv_ideas')
    ]
