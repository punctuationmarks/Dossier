from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('upload-csv-dossiers/', views.dossiers_upload_csv, name='dossier_upload_csv'),
    path('upload-csv-thoughts/', views.thoughts_upload_csv, name='thoughts_upload_csv')
    ]
