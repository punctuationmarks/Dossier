from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('upload-csv-dossiers/', views.upload_csv_dossier, name='upload_csv_dossier'),
    path('upload-csv-thoughts/', views.upload_csv_thoughts, name='upload_csv_thoughts'),
    path('upload-csv-ideas/', views.upload_csv_ideas, name='upload_csv_ideas')
    ]
